# Changelog

## [0.2.0](https://github.com/XJTU-ICP/FullereneDataParser/compare/v0.1.0...v0.2.0) (2022-09-29)


### Features

* **drawcage:** api for optional axes of matplotlib. ([8d78ed3](https://github.com/XJTU-ICP/FullereneDataParser/commit/8d78ed35e3bfc40b23688026e0082031c8ea27b1))
* **xcsi:** add poav orbital calculation. ([010778c](https://github.com/XJTU-ICP/FullereneDataParser/commit/010778c3ee0a2424dbd089a82da8b3c1633ebf2b))
* **xcsi:** calculation examples of csi with orbitals. ([eac3a3e](https://github.com/XJTU-ICP/FullereneDataParser/commit/eac3a3e692bf04482b1b8d93c4cdcdc41c0927ed))
* **xcsiwork:** draw results of xcsi models with angle/distance/adjmask. And schnet, spookynet. ([76adf97](https://github.com/XJTU-ICP/FullereneDataParser/commit/76adf971c3aac6d8438efd445097c310c2796e33))


### Bug Fixes

* **adj2spiral:** fix bug for system size and file extension. ([4f1bab1](https://github.com/XJTU-ICP/FullereneDataParser/commit/4f1bab1522eaa5afecad1a596bfa5c16f2b97b3c))
* **adj2spiral:** fix not read any comment from xyz file. ([b30e77d](https://github.com/XJTU-ICP/FullereneDataParser/commit/b30e77db409710cc2b2ecdfd692be4ec5f6c83a4))
* **atomadj:** fix wrong found result by natural cutoffs with first 3 shortest distances. ([46138a7](https://github.com/XJTU-ICP/FullereneDataParser/commit/46138a7f16ec0ceeac56b70e5f5e1bcecaaed265))
* **drawcage:** draw cage with a parallel edge. ([33b3dea](https://github.com/XJTU-ICP/FullereneDataParser/commit/33b3dea41a1e51736776b5a5d5c3f84b740f55e8))
* **originalcsi:** fix napp calculation in origin csi. ([1138917](https://github.com/XJTU-ICP/FullereneDataParser/commit/1138917a3ab1666ae037b20e0b24483159ad9bcf))

## [0.1.0](https://github.com/XJTU-ICP/FullereneDataPraser/compare/v0.0.2...v0.1.0) (2022-05-05)


### Features

* **adj2spiral:** Search spiral of an offering .gjf file from circle adj database. ([61a01fb](https://github.com/XJTU-ICP/FullereneDataPraser/commit/61a01fb141743ca05575173b70aa1541240d12c8))
* **example:** C2addonactor now using `spiral_slice` to control spiral number of tasks. ([1e9285e](https://github.com/XJTU-ICP/FullereneDataPraser/commit/1e9285e7be596c5434ed4d9186faf70c3ab5d3ce))
* **example:** C2addonactor now using `spiral_slice` to control spiral number of tasks. ([5b91c52](https://github.com/XJTU-ICP/FullereneDataPraser/commit/5b91c5206a9ab0f75a35ba983ca51f71e1c647a8))
* **example:** electron population of graph. ([9811ed5](https://github.com/XJTU-ICP/FullereneDataPraser/commit/9811ed5aa385cb0b34b63b48a429dd71a76ba491))
* **extend_csi:** add parameter `all_xyz` to read and calculate all xyz coordinations from xyz_dir's files. ([c20e4de](https://github.com/XJTU-ICP/FullereneDataPraser/commit/c20e4de22b20428ffa98979f62eaf65e418358d3))


### Bug Fixes

* **cage draw:** centralize the molecule before calculating layout. ([bc0dade](https://github.com/XJTU-ICP/FullereneDataPraser/commit/bc0dadefa5f7a573361f3756a8db8b0a808bafd9))
* **cage:** get circle_vertex_list with property but not callable. ([758dbf4](https://github.com/XJTU-ICP/FullereneDataPraser/commit/758dbf42b8596dd8f7167a007cede81dda76e794))
* **draw graph:** let the draw graph function work. ([aed6408](https://github.com/XJTU-ICP/FullereneDataPraser/commit/aed6408c249c13521c7c8bbac3b824e4a9331f32))
