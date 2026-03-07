import osmnx as ox
import geopandas as gpd
import os

def download_drainage_data(place_name, tags=None, output_path="data/drainage_raw.gpkg"):
    """
    Downloads waterway/drainage data from OSM for a given place.
    """
    if tags is None:
        tags = {
            'waterway': ['drain', 'ditch', 'stream', 'canal'],
            'man_made': ['pipeline', 'sewer']
        }
    
    print(f"Downloading data for {place_name} with tags {tags}...")
    
    try:
        # Get data by place name
        # We use geometries_from_place to get line features
        gdf = ox.features_from_place(place_name, tags=tags)
        
        if gdf.empty:
            print("No data found for the given tags.")
            return None
        
        # Filter for LineString and MultiLineString to represent pipelines
        gdf = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]
        
        # Save to GeoPackage
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        gdf.to_file(output_path, driver="GPKG")
        print(f"Data saved to {output_path}")
        print(f"Total features: {len(gdf)}")
        return gdf
        
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

if __name__ == "__main__":
    # Example study area: Velachery, Chennai
    study_area = "Velachery, Chennai, Tamil Nadu, India"
    download_drainage_data(study_area)
