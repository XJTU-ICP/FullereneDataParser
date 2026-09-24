# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : singleuse.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #
import ase
from ase.io.xyz import simple_read_xyz
import numpy as np
import torch
from lightMolNet import Properties
from lightMolNet.Struct.nn.schnet import SchNetLong
from lightMolNet.data.atomsref import get_refatoms, refat_xTB
from lightMolNet.data.dataloader import _collate_aseatoms_with_cuda, _collate_aseatoms
from lightMolNet.datasets.LitDataSet.xtbgraddataset import XtbGradDataSet
from lightMolNet.net import LitNet
from tqdm import tqdm
from lightMolNet.caculator import torchCaculator
from fullerenedataparser.io.xyz import simple_read_xyz_xtb

atomrefs = get_refatoms(refat_xTB, Properties.energy_U0, z_max=18)

Batch_Size = 128
USE_GPU = 0
statistics = False

scheduler = {"_scheduler": torch.optim.lr_scheduler.CyclicLR,
             "base_lr": 1e-9,
             "max_lr": 1e-4,
             "step_size_up": 10,
             "step_size_down": 50,
             "cycle_momentum": False
             }

ckpt_path = r"E:\#Projects\#Research\0623-xtbfuller-SchNet-longinter\output20210623\lightning_logs\version_0\checkpoints\FullNet-epoch=662-val_loss=0.0000.ckpt"
state_dict = torch.load(ckpt_path)
model = LitNet(representNet=[SchNetLong],
               batch_size=Batch_Size,
               learning_rate=1e-5,
               datamodule=None,
               scheduler=scheduler,
               atomref=atomrefs)
model.load_state_dict(state_dict["state_dict"])
if USE_GPU:
    model.to(device="cuda")
model.freeze()

for item in list(simple_read_xyz_xtb(r"D:\CODE\#DATASETS\FullDB\xTB2070\C20\C20_000000001opt.xyz")):
    atoms = item
    atoms.calc=torchCaculator(net=model)
    print(atoms.get_potential_energy())
