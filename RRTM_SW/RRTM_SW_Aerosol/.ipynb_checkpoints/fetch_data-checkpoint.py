import subprocess
import datetime

# Function to generate URLs for each day of the year 2023
def generate_urls():
    base_url = "https://e4ftl01.cr.usgs.gov/MOTA/MCD43C3.061/"
    for day in range(1, 366):  # Assuming a non-leap year
        date_str = datetime.date(2023, 1, 1) + datetime.timedelta(days=day-1)
        url = base_url + date_str.strftime("%Y.%m.%d") + "/"
        yield url

# Main function to call wget for each URL
def main():
    username = "oliviasalaben"
    password = "phN@Y6q*_K3B4h9"
    for url in generate_urls():
        subprocess.run(["wget", "--user=" + username, "--password=" + password, "-r", "-np", "-nc", "-nH", "--cut-dirs=3", "--accept=*.hdf", url])

if __name__ == "__main__":
    main()
