import random

class MT19937Reverse:
    def unshiftRight(self, x, shift):
        res = x
        for _ in range(32):
            res = x ^ res >> shift
        return res

    def unshiftLeft(self, x, shift, mask):
        res = x
        for _ in range(32):
            res = x ^ (res << shift & mask)
        return res

    def untemper(self, v):
        v = self.unshiftRight(v, 18)
        v = self.unshiftLeft(v, 15, 0xEFC60000)
        v = self.unshiftLeft(v, 7, 0x9D2C5680)
        v = self.unshiftRight(v, 11)
        return v

    def reverse(self, outputs, forward=True):
        assert len(outputs) >= 624

        ivals = [self.untemper(outputs[i]) for i in range(624)]

        result_state = None
        if len(outputs) >= 625:
            challenge = outputs[624]
            for i in range(1, 626):
                state = (3, tuple(ivals + [i]), None)
                r = random.Random()
                r.setstate(state)
                if challenge == r.getrandbits(32):
                    result_state = state
                    break
        else:
            result_state = (3, tuple(ivals + [624]), None)

        rand = random.Random()
        rand.setstate(result_state)

        if forward:
            for i in range(624, len(outputs)):
                assert rand.getrandbits(32) == outputs[i]

        return rand
