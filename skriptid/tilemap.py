class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3+i)+';10'] = {'type': 'grass', 'variant': 1, 'pos': (3+i, 10)} #position of 3 to 12 on the X 
                                                                                            #and 10 on the y ehk horisontaalne joon murul
            self.tilemap['10;'+str(5+i)] = {'type': 'grass', 'variant': 1, 'pos': (10, 5+i)} 

    def render(self, surf):
        for loc in self.tilemap:
            tile = self. tilemap[loc]
            surf. blit(self.game.assets[tile['type']])