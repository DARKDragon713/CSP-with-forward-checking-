import sys

def main():
    # Read input data
    M = int(sys.stdin.readline())
    min_price, max_price = map(int, sys.stdin.readline().split())
    cities = sys.stdin.readline().split()
    stays = list(map(int, sys.stdin.readline().split()))

    flights = []
    for _ in range(M):
        o, d, day, price = sys.stdin.readline().split()
        flights.append((o, d, int(day), int(price)))

    # number of flight legs
    K = len(cities) - 1

    # Build domains: organize flights by their leg in the trip
    domains = [[] for _ in range(K)]
    for i in range(K):
        for f in flights:
            if f[0] == cities[i] and f[1] == cities[i + 1]:
                domains[i].append((f[2], f[3]))  # (day, price)

    print(f"Initialized search space for {K} legs.")

if __name__ == "__main__":
    main()
