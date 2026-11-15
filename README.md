\# GeoAI Land Cover Segmentation



Semantic segmentation of buildings, woodland, water and roads from aerial imagery,

with results exported as georeferenced data for GIS analysis.



\## Week 1: Data Exploration



\*\*Dataset\*\*: \[LandCover.ai v1](https://landcover.ai.linuxpolska.com/)

(aerial orthophotos of Poland, CC BY-NC-SA 4.0)



\- Images: 41 GeoTIFFs (33 at 0.25 m, 8 at 0.5 m), total area 216.27 km²

\- CRS: custom Transverse Mercator (WGS84 datum), equivalent to EPSG:2180



| Class | Pixel ratio |

|---|---|

| background | 58.13% |

| building | 0.86% |

| woodland | 33.32% |

| water | 6.08% |

| road | 1.62% |



The computed ratios match the official class areas, confirming the data was read correctly.



\*\*Observations\*\*

\- Strong class imbalance: buildings cover only 0.86% of pixels, about 1/39 of woodland.

&#x20; A model that ignores buildings and roads could still reach \~97% pixel accuracy,

&#x20; so I will evaluate with per-class IoU instead of accuracy.

\- Roads appear as thin lines only a few pixels wide, so they may be hard to segment.

\- The masks align with OpenStreetMap in QGIS, so the georeferencing is reliable.



!\[Mask aligned with OpenStreetMap](outputs/week1\_osm\_check.png)

