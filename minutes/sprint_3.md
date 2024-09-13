# Real Estate Consulting Project
## Minutes: 12/09/2024 14:15

**Group Members:** Anshan, Jenny, Vivian, Zirui (Eddie)

**Agenda**
- Oldlistings cannot be used anymore, use Excel sheet
    - Problem: cannot perform distance calculations as individual addresses are not given
        - Idea: Use centre of area to calculate distance
- Coordinator to release an announcement regarding oldlistings soon? 
- Discussed number of properties to scrape per SA2/suburb
    - For now, 500 per area (can reduce if we run into computational issues)
- Might run into future issues regarding SA2 vs suburbs
- Need to edit Domain scraping code
    - Domain has a page limit of 50 (1000 properties per search)
        - Solution: decrease search region
    - Properties were sorted by price (biased sampling)
        - Solution: re-scrape with sorting filter removed

**To-do**
- Eddie: continue creating postcode/suburb resource
- Anshan: edit Domain scrape code
- Vivian: preprocess external datasets
- Jenny: preprocess Domain data
- Eddie and Anshan: calculate distances using OpenRouteService

**Signed:** Anshan, Jenny, Vivian, Zirui