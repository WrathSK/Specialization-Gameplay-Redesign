#!/usr/bin/env python3
"""Build approved B268 raw icons with Pillow; no game, source PNG or config writes.

Original PNGs stay in ignored local storage. Native claim district artwork remains engine-owned; the runtime UI adds the
approved claim mark as a separate child Image.
The build emits lossless BGRA8 DDS, SQL and a pixel/hash verification manifest.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ATLAS='ICON_ATLAS_SPC_RAW'

def digest(data): return hashlib.sha256(data).hexdigest()

def write_dds(path, image):
    image=image.convert('RGBA');w,h=image.size
    header=b'DDS '+struct.pack('<7I',124,0x100f,h,w,w*4,0,0)+bytes(44)
    header+=struct.pack('<8I',32,0x41,0,32,0xff0000,0xff00,0xff,0xff000000)
    header+=struct.pack('<5I',0x1000,0,0,0,0)
    assert len(header)==128
    data=header+image.tobytes('raw','BGRA');path.write_bytes(data)
    # Decode through Pillow's DDS reader, independently of the writer's byte order.
    with Image.open(path) as decoded:
        assert decoded.convert('RGBA').tobytes()==image.tobytes(),path.name
    return {'file':path.name,'sha256':digest(data),'bytes':len(data),'width':w,'height':h,'format':'BGRA8','decoded_pixel_match':True}

def bounds(image):
    return image.getchannel('A').point(lambda x:255 if x>=8 else 0).getbbox()

def contain(image,size,box=None,occupancy=.86):
    box=box or bounds(image)
    assert box,'Empty artwork'
    crop=image.crop(box)
    limit=max(1,round(size*occupancy));scale=limit/max(crop.size)
    dims=tuple(max(1,round(n*scale))for n in crop.size)
    crop=crop.resize(dims,Image.Resampling.LANCZOS)
    # Remove invisible RGB fringe while preserving all visible source colors.
    crop.paste((0,0,0,0),mask=crop.getchannel('A').point(lambda a:255 if a==0 else 0))
    out=Image.new('RGBA',(size,size))
    out.alpha_composite(crop,((size-dims[0])//2,(size-dims[1])//2))
    return out

def sql(manifest,files):
    lines=['-- B268: approved raw art only; native/global definitions are untouched.']
    for f in files:
        lines.append("INSERT OR REPLACE INTO IconTextureAtlases(Name,IconSize,IconsPerRow,IconsPerColumn,Filename) VALUES ('%s',%d,5,4,'%s');"%(ATLAS,f['width']//5,f['file']))
    defs=[(i['icon'],i['index'])for i in manifest['items']]
    for claim in manifest['claims']:
        lines.append("INSERT OR REPLACE INTO IconDefinitions(Name,Atlas,[Index]) SELECT 'ICON_PROJECT_SPC_CLAIM_%s',Atlas,[Index] FROM IconDefinitions WHERE Name='ICON_DISTRICT_%s';"%(claim['key'],claim['district']))
    units=[('EXPEDITION_SPY',0),('RESTRUCTURING_TEAM',1)]+[('CREW_'+str(t),2)for t in(250,420,750,1000,1360)]
    for unit,index in units:
        name='ICON_UNIT_SPC_'+unit
        lines.append(f"UPDATE IconDefinitions SET Atlas='{ATLAS}', [Index]={index} WHERE Name='{name}' OR Name GLOB '{name}_*';")
        defs += [(name+suffix,index)for suffix in('','_PORTRAIT','_WHITE','_FOW')]
    lines.append("UPDATE IconDefinitions SET Atlas='%s',\"Index\"=2 WHERE Name GLOB 'ICON_PROJECT_SPC_CREW_*';"%ATLAS)
    defs += [('ICON_PROJECT_SPC_'+name,index)for name,index in [('COMMERCIALIZATION',11),('CAPITAL_INVESTMENT',12),('DEVELOPMENT_INVESTMENT',13),('ERA_DIALOGUE',14),('ENGINEERING_STUDY',15)]]
    for name,index in defs:
        lines.append("INSERT OR REPLACE INTO IconDefinitions(Name,Atlas,\"Index\") VALUES ('%s','%s',%d);"%(name,ATLAS,index))
    return '\n'.join(lines)+'\n'

def build(args):
    m=json.loads(args.manifest.read_text());images={}
    for item in m['items']:
        path=args.source/item['file'];data=path.read_bytes()
        assert digest(data)==item['sha256'],'Source hash mismatch: '+item['id']
        with Image.open(path)as im:images[item['index']]=im.convert('RGBA')
    # Both investment steps share one transform so the approved main subject
    # remains at exactly the same position/scale beneath its different symbol.
    pair=[bounds(images[n])for n in(9,10)]
    pairbox=(min(x[0]for x in pair),min(x[1]for x in pair),max(x[2]for x in pair),max(x[3]for x in pair))
    args.output.mkdir(parents=True,exist_ok=True)
    files=[]
    for size in m['sizes']:
        sheet=Image.new('RGBA',(size*m['columns'],size*m['rows']))
        for index,im in images.items():
            icon=contain(im,size,pairbox if index in(9,10)else None)
            sheet.alpha_composite(icon,((index%m['columns'])*size,(index//m['columns'])*size))
        files.append(write_dds(args.output/f'SPC_Raw_Icons_{size}.dds',sheet))
    args.sql.write_text(sql(m,files))
    record={'build':m['build'],'source_manifest_sha256':digest(args.manifest.read_bytes()),'transforms':'Alpha>=8 bounds, aspect-preserving contain86%, centered; investment pair union bounds; native district stays in engine; approved mark overlaid by UI. No repaint/whitening/shape edits.','files':files,'total_bytes':sum(i['bytes']for i in files)}
    record['bundle_sha256']=digest(''.join(f['file']+':'+f['sha256']+'\n'for f in files).encode())
    args.review.write_text(json.dumps(record,indent=2)+'\n')
    if args.preview:
        out=Image.new('RGB',(1000,((len(images)+3)//4)*180),'#173044');d=ImageDraw.Draw(out)
        for index,im in images.items():
            x,y=(index%4)*250,(index//4)*180
            big=contain(im,100,pairbox if index in(9,10)else None);out.paste(big,(x+8,y+8),big)
            for n,size in enumerate((20,32,38)):
                small=contain(im,size,pairbox if index in(9,10)else None);out.paste(small,(x+118+n*43,y+55-size//2),small)
            item=next((i for i in m['items']if i['index']==index),None)
            title=(item['id']+' '+item['key'])if item else'UNKNOWN'
            d.text((x+9,y+125),title,fill='white');d.text((x+9,y+143),'100 / 20 / 32 / 38 px',fill='#a9bfd3')
        out.save(args.preview)
    print(json.dumps({'files':len(files),'total_bytes':record['total_bytes'],'bundle_sha256':record['bundle_sha256'],'decoded_pixels':'MATCH'}))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--manifest',type=Path,default=HERE/'raw_icons_manifest.json')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--sql',type=Path,required=True)
    p.add_argument('--review',type=Path,required=True)
    p.add_argument('--preview',type=Path)
    build(p.parse_args())

if __name__=='__main__':main()
