import pandas as pd
import itertools
from random import sample, choice, choices
from copy import deepcopy

import plotly.graph_objects as go

from icecream import ic 
ic.configureOutput(includeContext=True)



PADS_RESSOURCES = [
    ("GNDA", "grd_analog"),
    ("GNDD", "grd_digital"),
    ("HVIN", "hv_input"),
    ("HFRES", "hf_resol"),
    ("DIGIO", "io_digital"),
    ("ANIO", "io_analog")
    ]

COMPONENTS = [
    "RESITOR",
    "CAPACITOR",
    "RELAY",
    "FLUX_CAPACITOR",
]



class Site():
    def __init__(self, x_pad, y_pad, die_size, pad_size) -> None:
        self.x_pad = x_pad
        self.y_pad = y_pad
        self.die_size = die_size
        self.pad_size = pad_size
        self.pad_name = None
        self.rsc = None
        self.name = None
        self.component = None
        

    def attribute_pad_name(self):
        ls = [
            choice(PADS_RESSOURCES) for x in range(len(self.x_pad))
        ]
        self.pad_name = [x[0] for x in ls]
        self.rsc = [x[1] for x in ls]

    def attribute_component(self):
        self.component=[]
        for n in range(len(self.x_pad)):
            ch = choices([False, True], weights=[5,1], k=1)[0]
            if ch:
                self.component.append(choice(COMPONENTS))
            else:
                self.component.append(None)

    def copy_site(self, delta_x, delta_y):
        self.attribute_pad_name()
        self.attribute_component()
        copy = deepcopy(self)
        copy.x_pad = [x+delta_x for x in self.x_pad]
        copy.y_pad = [y+delta_y for y in self.y_pad]
        return copy
    
class ProbeCard():
    def __init__(self, site, layout, skip = (1,1)) -> None:
        self.site = site
        self.layout = layout #(x, y)
        self.skip = skip #(x, y) => (0,0) for no skip
        self.data = {}
        self.df = None

    def get_tips_coords(self):
        sites = []
        n = 0

        for col in range(self.layout[1]):
            if len(sites) == 0:
                copy = self.site.copy_site(0,0)
                copy.name = n
                sites.append(copy)
            else:
                copy = sites[-1].copy_site(self.site.die_size*(self.skip[0]+1),0)
                copy.name = n
                sites.append(copy)
            n += 1
        for row in range(self.layout[0]-1):
            for _ in range(self.layout[1]):
                copy = sites[-self.layout[1]].copy_site(0,self.site.die_size*(self.skip[1]+1))
                copy.name = n
                sites.append(copy)
                n+=1
        self.data["x_pad"] = list(itertools.chain.from_iterable([s.x_pad for s in sites]))
        self.data["y_pad"] = list(itertools.chain.from_iterable([s.y_pad for s in sites]))
        self.data["pad_name"] = list(itertools.chain.from_iterable([s.pad_name for s in sites]))
        self.data["rsc"] = list(itertools.chain.from_iterable([s.rsc for s in sites]))
        self.data["component"] = list(itertools.chain.from_iterable([s.component for s in sites]))
        self.data["tip_number"] = [x for x in range(len(self.data['x_pad']))]
        ic(f"Data generated, tip count is {len(self.data['x_pad'])}")

    def init_pc(self):
        self.get_tips_coords()
        self.df = self.get_pc_df()


    def get_str_route(self, row):
        if isinstance(row["component"], str):
            route = f"{row['pad_name']}---{row['component']}---{row['rsc']}"
        else : 
            route = f"{row['pad_name']}---{row['rsc']}"
        return route

    def get_pc_df(self):
        df = pd.DataFrame.from_dict(self.data)
        df["route"] = df.apply(self.get_str_route, axis=1)
        self.df = df
        return df

    def get_scatter(self):
        df = self.get_pc_df()
        fig = go.Figure(go.Scatter(x=df.x_pad,
                        y=df.y_pad,
                        mode="markers",
                        hoverinfo="text",
                        hovertext=df.route),
                        )
        fig.update_layout(title={"text" : "ProbeMap",
                                 "x":0.5,
                                 "y" : 0.9,
                                 "yanchor" : "bottom"})
        ic(df)
        fig.show()

    def export_to_xlsx(self):
        self.df.to_excel("pc_data.xlsx")


def site_generator(
        die_size,pad_size,fill=0.5):
    
    #square die for easy test
    tpr = int((die_size/pad_size)*fill) #TipsPerRow
    row_indexes = list(range(0, die_size, pad_size))
    #generate map
    x_pad = []
    y_pad = []
    for _ in row_indexes:
        x = 0 if len(x_pad) == 0 else x_pad[-1] + pad_size
        y_list = sample([x for x in range(0, die_size, pad_size)], k=tpr)
        for y in y_list:
            x_pad.append(x)
            y_pad.append(y)
    
    return Site(x_pad, y_pad, die_size, pad_size)


    
        




        
        



    