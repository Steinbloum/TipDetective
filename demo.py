from FakeGenerators import site_generator, ProbeCard

"""For easy testing purposes, die size and pad size are square"""

"""INPUT DIE SETTINGS"""
die_size = 3000 #microns
pad_size = 70 #microns
fill_rate = 0.4 #0=>1

"""INPUT PC SETTINGS"""
layout = (3,4) #(x, y)
skip = (1,1) #(x, y) , 0 for no skip


pc = ProbeCard(site_generator(die_size, pad_size, fill_rate),
               layout,skip)
pc.init_pc()
pc.get_scatter()
pc.export_to_xlsx()











