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
        # Get data by place name or point
        if isinstance(place_name, (list, tuple)):
            print(f"Downloading data around point {place_name}...")
            gdf = ox.features_from_point(place_name, tags=tags, dist=1500)
        else:
            print(f"Downloading data for place '{place_name}'...")
            try:
                gdf = ox.features_from_place(place_name, tags=tags)
            except Exception as e:
                print(f"Place search failed: {e}. Trying geocode point + buffer...")
                point = ox.geocoder.geocode(place_name)
                gdf = ox.features_from_point(point, tags=tags, dist=1500)
        
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
