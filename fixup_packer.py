
class TexturePackerAtlas:
    def __init__(self, fname):
        self.names = []
        self.infos = []
        self.read(fname)

    def read(self, fname):
        with open(fname) as fp:
            groups = []
            for line in fp:
                if not ':' in line:
                    groups.append([])
                groups[-1].append(line.strip())
            for grp in groups:
                self.names.append(grp[0])
                self.infos.append({})
                for it in grp[1:]:
                    fields = it.split(':')
                    self.infos[-1][fields[0].strip()] = fields[1].strip()

    def write(self, fname):
        with open(fname, "w") as fp:
            fp.write(self.names[0] + "\n")
            for key, val in self.infos[0].items():
                fp.write("{}: {}\n".format(key, val))
            for name, info in zip(self.names[1:], self.infos[1:]):
                fp.write(name + "\n")
                for key, val in info.items():
                    fp.write("  {}: {}\n".format(key, val))

old_to_new_names = {
  'non': 'NonAtkEffect'
}
OLD_NAME_LENGTH = 3

if __name__ == '__main__':
    src = 'FixupSprites.txt'
    dst = 'GameplaySprites.txt'
    dstPng = 'GameplaySprites.png'
    atlas = TexturePackerAtlas(src)
    for i, grp in enumerate(zip(atlas.names, atlas.infos)):
        name, info = grp
        prefix = name[:OLD_NAME_LENGTH]
        if prefix in old_to_new_names:
            new_name = old_to_new_names[prefix]
            idx = int(name[OLD_NAME_LENGTH:])
            info['index'] = idx
            atlas.names[i] = new_name 
    atlas.names[0] = 'GameplaySprites.png'
    atlas.write(dst)
