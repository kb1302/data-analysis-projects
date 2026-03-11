# Stanford Startup & Unicorn Founder Analysis

Data analysis scripts developed during a research assistantship at the Stanford Graduate School of Business, supporting published research on venture-backed startups and founder demographics.

## Overview

This project analyzes a large dataset of founders at unicorn companies — privately held startups valued at over $1 billion — to identify demographic patterns, educational backgrounds, and social network effects. Findings contributed to 50+ published research posts reaching 90,000+ readers across LinkedIn and other platforms.

## Scripts

| File | Description |
|---|---|
| `AgeJoinedUnicorns.py` | Cleans and visualizes the age distribution of founders at the time their companies reached unicorn status |
| `UF_foreign_university.py` | Filters and aggregates founder data by university country of origin, producing ranked tables of international institutions |
| `get_results.py` | Groups and counts university representation across unicorn and repeat-success (RS) founder cohorts |
| `homophily_finder.py` | Detects co-founder pairs who attended the same university during overlapping periods, with logic to estimate missing enrollment dates by degree type |

## Tools & Libraries

Python, Pandas, Matplotlib, NumPy, openpyxl

## Notes

Raw datasets are not included as they are proprietary to the research institution. Scripts are shared to demonstrate analytical approach and coding methodology.
