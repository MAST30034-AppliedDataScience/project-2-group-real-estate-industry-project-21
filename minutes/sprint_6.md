# Real Estate Consulting Project
## Minutes: 03/10/2024 14:15

**Group Members:** Anshan, Jenny, Vivian, Zirui (Eddie)

**Agenda**
- Presentation slides due on Monday
    - Eddie prepared slide template
    - Anshan brainstormed content for presentation
    - Vivian to continue making maps
    - Jenny has some visualisations from analysis/modelling
- Datasets (cleaning/curating) and modelling mostly done
    - Model performance improves significantly when income and population is used with Domain data
    - Linearity assumptions for linear regression do not seem good
    - Waiting on distance calculations to finish running
    - Make future predictions using historical rent data
- In regards to the big 3 questions
    1. Predict future rental prices by multiplying current predictions by rental rate increase
    2. Growth rate can refer to both population growth and rental price growth; answer both
    3. Need to finalise affordability and liveability metrics for each postcode
        - Affordability: average rent / median income
        - Liveability: calculate a liveability score for each property in the suburb then average. 
        - Liveability score: for each amenity type, +1 if there is an amenity within 1km, +1/2 if there is an additional amenity of the same type, +1/3 if there is another amenity of the same type, etc. then multiply by weight
            - Weights: hospital = 1, parks = 2, shopping districts = 3, schools = 4, train stations = 4, supermarkets = 4
- Scale of analysis changed to postcodes instead of suburbs (easier to merge datasets)
- Need to merge Jenny's branch with main
- Removed API key from Git

**Task Allocation**
- Everyone to work on presentation together (hold an additional meeting over the weekend)
- Finish analysis and modelling (Jenny) with completed distance data (from Eddie)
- Combine predictions with historical rent and population data to make future predictions (Anshan + Vivian) 
- Apply liveability metric (Anshan)
- Apply affordability metric + make maps of postcode statistics (Vivian)

**Signed:** Anshan, Jenny, Vivian, Zirui