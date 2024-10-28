import argparse
from realtorca import get_property_list_by_city

def main():
    parser = argparse.ArgumentParser(description='Get property list by city')
    parser.add_argument('city', type=str, help='City name')
    args = parser.parse_args()

    get_property_list_by_city(args.city)

if __name__ == '__main__':
    main()
