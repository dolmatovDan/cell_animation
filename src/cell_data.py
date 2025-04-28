import numpy as np


class CellData:
    def __init__(self, a: np.array, d: np.array, teta1: float, teta2: float,
                 gamma: float):
        self.a = a / np.linalg.norm(a)
        self.d = d / np.linalg.norm(d)
        self.b = np.cross(a, d)
        self.cosphi = np.dot(a, d)
        self.phi = np.arccos(self.cosphi)
        self.teta1 = teta1
        self.teta2 = teta2
        self.gamma = gamma

    def get_childs(self):
        posd = np.cos(self.teta1) * self.d + np.sin(self.teta1) * self.b
        negd = np.cos(self.teta1) * self.d - np.sin(self.teta1) * self.b

        a_ort = self.a - self.cosphi * self.d
        A = (1 + self.cosphi**2 * self.gamma**2 - self.gamma**2)**0.5
        if self.cosphi < 0:
            A *= -1

        posa = self.gamma * a_ort + A * \
            (np.cos(self.teta2) * self.d + np.sin(self.teta2) * self.b)

        nega = self.gamma * a_ort + A * \
            (np.cos(self.teta2) * self.d - np.sin(self.teta2) * self.b)

        pos = CellData(posa, posd, self.teta1, self.teta2, self.gamma)
        neg = CellData(nega, negd, self.teta1, self.teta2, self.gamma)
        return pos, neg

    def calc_dxy(self):
        return self.d[0], self.d[1]
