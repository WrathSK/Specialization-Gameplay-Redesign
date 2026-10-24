"""B271 bounded TRAIN summary; observations are not engine accrual attribution."""
from collections import defaultdict

class TurnTimingEvidence:
    LIMIT = 4096
    def __init__(self):
        self.rows = []
        self.dropped = 0
    def add(self, fields):
        if fields.get('stage') not in {'TREASURY_POINT','TIMING_NETWORK_VERIFIED','TURN_EVENT_COUNTS','EVENT_ORDER_START','EVENT_ORDER_BATCH','EVENT_ORDER_END','EVENT_ORDER_HOOKS'}:
            return
        if len(self.rows) >= self.LIMIT:
            self.dropped += 1
            return
        self.rows.append(dict(fields))
    def summary(self):
        lines = ['timing_scope: observer callback order; first observed balance change is not proof of accrual; missing points/order remain UNKNOWN']
        def seq(row):
            try: return int(row.get('observationSeq', '-1'))
            except ValueError: return -1
        groups = defaultdict(list)
        for row in self.rows:
            groups[row.get('observationEpoch','UNKNOWN')].append(row)
        for epoch, rows in groups.items():
            rows.sort(key=seq)
            balances = {}; changed = set(); windows = {}
            for row in rows:
                stage = row['stage']; cycle = row.get('observationCycle','?'); side = row.get('observerSide','?')
                if stage == 'TREASURY_POINT':
                    balance = row.get('goldBalance','UNKNOWN'); point = row.get('point','?')
                    previous = balances.get(cycle)
                    change = ''
                    try:
                        from decimal import Decimal, InvalidOperation
                        if previous is not None and Decimal(balance) != Decimal(previous) and cycle not in changed:
                            changed.add(cycle)
                            # Compare to network confirmation within this observed cycle only.
                            verified = [seq(v) for v in rows if v['stage']=='TIMING_NETWORK_VERIFIED' and v.get('observationCycle')==cycle]
                            before = [v for v in verified if v < seq(row)]
                            after = [v for v in verified if v > seq(row)]
                            relation = 'AFTER_OBSERVED_VERIFIED' if before else 'BEFORE_OBSERVED_VERIFIED' if after else 'UNKNOWN'
                            change = ' FIRST_OBSERVED_CHANGE relation='+relation
                    except (InvalidOperation, ValueError):
                        change = ' balance_comparison=UNKNOWN'
                    balances[cycle] = balance
                    lines.append(f'treasury epoch={epoch} cycle={cycle} T{row.get("turn","?")} seq={seq(row)} {point} gold={balance} yield={row.get("goldYield","UNKNOWN")} network={row.get("networkAvailability","UNKNOWN")}/{row.get("networkRevalidation","UNKNOWN")} lastVerified={row.get("lastVerifiedSeq","?")}{change}')
                elif stage == 'TURN_EVENT_COUNTS':
                    lines.append(f'event_counts epoch={epoch} T{row.get("turn","?")} {row.get("point","?")} callback_counts_not_native_events {row.get("counterBatch","UNKNOWN")}')
                elif stage == 'EVENT_ORDER_HOOKS':
                    lines.append(f'event_order_hooks {epoch} {side} unavailable={row.get("eventBatch","UNKNOWN")}')
                elif stage == 'EVENT_ORDER_START':
                    # One active window per side. Never use arrival time to reorder events.
                    if side in windows:
                        lines.append(f'event_order {epoch} {side} previous_window=INCOMPLETE')
                    windows[side] = {'start': True, 'received': 0}
                elif stage == 'EVENT_ORDER_BATCH':
                    window = windows.setdefault(side, {'start': False, 'received': 0})
                    window['received'] += len(row['eventBatch'].split('|')) if row.get('eventBatch') else 0
                elif stage == 'EVENT_ORDER_END':
                    window = windows.pop(side, {'start': False, 'received': 0})
                    had_start = window['start']
                    received = window['received']
                    expected = row.get('eventTotal','UNKNOWN')
                    complete = had_start and str(received)==expected and row.get('reason')=='LOCAL_BEGIN' and row.get('observerErrors','0')=='0'
                    lines.append(f'event_order {epoch} {side} reason={row.get("reason","?")} truncated={row.get("eventTruncated","UNKNOWN")} received={received} expected={expected} complete={complete} publish={row.get("eventPublishCount","?")} observerErrors={row.get("observerErrors","UNKNOWN")} start_missing={not had_start}')
            for side,n in windows.items():
                lines.append(f'event_order {epoch} {side} INCOMPLETE received={n["received"]} end_missing=true')
            points = defaultdict(set)
            for row in rows:
                if row['stage']=='TREASURY_POINT': points[row.get('observationCycle','?')].add(row.get('point'))
            required={'LOCAL_DEACTIVATED','FIRST_FOREIGN_ACTIVATED','GAME_PLAYER_STARTED','LOCAL_ACTIVATED','LOCAL_BEGIN','FIRST_PUBLISH_AFTER_BEGIN'}
            for cycle, seen in points.items():
                missing=sorted(required-seen)
                if missing: lines.append(f'treasury_missing epoch={epoch} cycle={cycle}: '+','.join(missing))
        if not self.rows: lines.append('timing_records: NONE (old build, window expired, or unavailable; not PASS)')
        if self.dropped: lines.append(f'timing_summary_truncated: {self.dropped}')
        return lines
