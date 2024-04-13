### Use Case: Business Directory Enrichment

**Scenario**: A business directory service collects raw data on businesses throughout South Africa. The data includes incomplete and inconsistent location information.

**Solution**: Utilize the script to automatically query the Google Maps Geocoding API to determine the exact province for each business and identify the closest major city based on a predefined list. This enriched data is then saved in a structured format.

**Benefit**: Enhances the accuracy and usability of the business directory, making it more valuable for users seeking local services and for businesses aiming to improve their visibility.

### Example Data

**Input CSV**:
```csv
Name,Location
The Corner Cafe, "Somerset West"
Joe's Butchery, "Kimberley"
Luxury Spa, "Sandton"
```

**Output CSV**:
```csv
Name,Location,Province,Closest City
The Corner Cafe, "Somerset West", "Western Cape", "Cape Town"
Joe's Butchery, "Kimberley", "Northern Cape", "Kimberley"
Luxury Spa, "Sandton", "Gauteng", "Johannesburg"
```

This script effectively standardizes and enriches business location data, facilitating improved search and filtering capabilities in a business directory application.