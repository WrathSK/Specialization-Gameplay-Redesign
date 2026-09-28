"""Isolated gate model, NOT Civ VI API mocks or shipped Gameplay.
Run with Python stdlib. Assumes an authoritative active-project set and a complete
blocker snapshot; does not prove the native engine can supply either contract.
"""
import copy
import unittest


class Gate:
    def __init__(self):
        self.active = {}  # city identity -> current activity token
        self.known = False
        self.revision = 0
        self.inflight = False

    def restore(self, authoritative):
        self.active = dict(authoritative or {})
        self.known = authoritative is not None
        self.revision += 1
        self.inflight = False

    def start(self, city, token):
        if self.active.get(city) != token:
            self.active[city] = token
            self.revision += 1

    def finish(self, city, token):
        if self.active.get(city) == token:
            del self.active[city]
            self.revision += 1

    def request(self, read, send, manual=True):
        if not manual or not self.known or not self.active or self.inflight:
            return 'NORMAL'
        revision = self.revision
        try:
            s = read()  # only on explicit request with active activities
            if not isinstance(s, dict) or s.get('complete') is not True:
                return 'NORMAL'
            if any(s.get(k) is not True for k in ('turn_ready', 'single_local', 'independent_checks_clear')):
                return 'NORMAL'
            # Never assume the first displayed notification is the whole set.
            if s.get('types') != {'PRODUCTION'} or not s.get('production_cities'):
                return 'NORMAL'
            if any(s['activities'].get(c) != self.active.get(c) or c not in self.active
                   for c in s['production_cities']):
                return 'NORMAL'
            if revision != self.revision or s.get('revision') != revision:
                return 'NORMAL'
        except (KeyError, TypeError, RuntimeError):
            return 'NORMAL'
        self.inflight = True  # before submission, preventing reentrant duplicates
        try:
            send()
        except RuntimeError:
            # Delivery uncertain: do not clear automatically and allow a replay.
            return 'SUBMISSION_UNKNOWN'
        return 'FORCE_REQUEST'


class GateModelTests(unittest.TestCase):
    def setUp(self):
        self.g = Gate()
        self.g.restore({})
        self.scans = 0
        self.sends = 0

    def snapshot(self):
        self.scans += 1
        return dict(complete=True, turn_ready=True, single_local=True,
                    independent_checks_clear=True, types={'PRODUCTION'},
                    production_cities=set(self.g.active), activities=dict(self.g.active),
                    revision=self.g.revision)

    def send(self):
        self.sends += 1

    def test_inactive_has_no_scan(self):
        for _ in range(3):
            self.assertEqual(self.g.request(self.snapshot, self.send), 'NORMAL')
        self.assertEqual((self.scans, self.sends), (0, 0))

    def test_active_only_explicit_click_then_deduplicated(self):
        self.g.start('A', 'a1')
        self.assertEqual(self.g.request(self.snapshot, self.send, manual=False), 'NORMAL')
        self.assertEqual(self.scans, 0)
        self.assertEqual(self.g.request(self.snapshot, self.send), 'FORCE_REQUEST')
        self.assertEqual(self.g.request(self.snapshot, self.send), 'NORMAL')
        self.assertEqual((self.scans, self.sends), (1, 1))

    def test_many_cities_one_completion_does_not_disarm_others(self):
        self.g.start('A', 'a1'); self.g.start('B', 'b1')
        self.g.finish('A', 'a1'); self.g.finish('A', 'a1')
        self.assertEqual(self.g.active, {'B': 'b1'})
        self.assertEqual(self.g.request(self.snapshot, self.send), 'FORCE_REQUEST')

    def test_stale_completion_cannot_remove_new_activity(self):
        self.g.start('A', 'old'); self.g.start('A', 'new')
        self.g.finish('A', 'old')
        self.assertEqual(self.g.active, {'A': 'new'})

    def test_finish_cancel_or_loss_last_disarms(self):
        for reason in ('complete', 'cancel', 'confirmed_owner_loss'):
            with self.subTest(reason=reason):
                self.g.restore({'A': reason}); self.g.finish('A', reason)
                self.assertEqual(self.g.request(self.snapshot, self.send), 'NORMAL')
        self.assertEqual((self.scans, self.sends), (0, 0))

    def test_other_blockers_including_lower_priority(self):
        self.g.start('A', 'a1')
        for kind in ('RESEARCH', 'CIVIC', 'UNIT', 'GOVERNMENT', 'UNKNOWN'):
            s = self.snapshot(); s['types'].add(kind)
            self.assertEqual(self.g.request(lambda: s, self.send), 'NORMAL')
        self.assertEqual(self.sends, 0)

    def test_unrelated_empty_city_and_wrong_token(self):
        self.g.start('A', 'a1')
        for other in ('unrelated', 'wrong_token'):
            s = self.snapshot()
            if other == 'unrelated':
                s['production_cities'].add('B')
            else:
                s['activities']['A'] = 'old'
            self.assertEqual(self.g.request(lambda: s, self.send), 'NORMAL')
        self.assertEqual(self.sends, 0)

    def test_independent_hd_or_unit_checks_not_bypassed(self):
        self.g.start('A', 'a1')
        for key in ('independent_checks_clear', 'turn_ready', 'single_local', 'complete'):
            s = self.snapshot(); s[key] = False
            self.assertEqual(self.g.request(lambda: s, self.send), 'NORMAL')
        self.assertEqual(self.sends, 0)

    def test_stale_or_unknown_snapshot(self):
        self.g.start('A', 'a1')
        s = self.snapshot(); s['revision'] -= 1
        for value in (s, None, {}, {'complete': True}):
            self.assertEqual(self.g.request(lambda: value, self.send), 'NORMAL')
        def fails():
            raise RuntimeError('unavailable')
        self.assertEqual(self.g.request(fails, self.send), 'NORMAL')
        self.assertEqual(self.sends, 0)

    def test_state_change_during_check_rejects(self):
        self.g.start('A', 'a1')
        def changed():
            s = self.snapshot(); self.g.finish('A', 'a1'); return s
        self.assertEqual(self.g.request(changed, self.send), 'NORMAL')
        self.assertEqual(self.sends, 0)

    def test_blocked_click_can_retry_after_user_resolves_blocker(self):
        self.g.start('A', 'a1'); s = self.snapshot(); s['types'].add('RESEARCH')
        self.assertEqual(self.g.request(lambda: s, self.send), 'NORMAL')
        self.assertEqual(self.g.request(self.snapshot, self.send), 'FORCE_REQUEST')
        self.assertEqual(self.sends, 1)

    def test_reload_rebuilds_only_authoritative_active_set(self):
        self.g.start('A', 'a1'); saved = copy.deepcopy(self.g.active)
        other = Gate()
        self.assertEqual(other.request(self.snapshot, self.send), 'NORMAL')
        other.restore(saved)
        self.assertEqual(other.active, {'A': 'a1'})
        other.restore({})
        self.assertEqual(other.request(self.snapshot, self.send), 'NORMAL')
        other.restore(None)
        self.assertFalse(other.known)
        self.assertEqual(self.sends, 0)

    def test_reentrant_or_uncertain_submission_not_replayed(self):
        self.g.start('A', 'a1')
        def submit():
            self.assertEqual(self.g.request(self.snapshot, self.send), 'NORMAL')
            raise RuntimeError('delivery unknown')
        self.assertEqual(self.g.request(self.snapshot, submit), 'SUBMISSION_UNKNOWN')
        self.assertEqual(self.g.request(self.snapshot, self.send), 'NORMAL')
        self.assertEqual(self.scans, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
