import sys

def main():
    # -----------------------------
    # Read input
    # -----------------------------
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

    # -----------------------------
    # Build domains
    # -----------------------------
    # domains[i] = all flights from cities[i] -> cities[i+1]
    domains = [[] for _ in range(K)]

    for i in range(K):
        for f in flights:
            if f[0] == cities[i] and f[1] == cities[i + 1]:
                domains[i].append((f[2], f[3]))  # (day, price)

    assignment = [None] * K

    # -----------------------------
    # Forward Checking
    # -----------------------------
    def forward_check(i):
        """
        Remove invalid flights from the *next* domain.
        Returns a list of removed values so we can undo later.
        """
        if i == K - 1:
            return []

        removed = []
        prev_day = assignment[i][0]

        # stays are packed like: min0 max0 min1 max1 ...
        min_stay = stays[2 * i]
        max_stay = stays[2 * i + 1]

        # Iterating on a copy since we mutate the real domain
        for flight in domains[i + 1][:]:
            day = flight[0]
            if not (prev_day < day and min_stay <= day - prev_day <= max_stay):
                domains[i + 1].remove(flight)
                removed.append(flight)

        return removed

    # -----------------------------
    # Backtracking Search
    # -----------------------------
    def backtrack(i):
        if i == K:
            # Only check budget at the end (doing it earlier prunes valid paths)
            total = sum(p for _, p in assignment)
            return min_price <= total <= max_price

        for value in domains[i]:
            # Local consistency with previous flight
            if i > 0:
                prev_day = assignment[i - 1][0]
                min_stay = stays[2 * (i - 1)]
                max_stay = stays[2 * (i - 1) + 1]

                # This check duplicates FC logic, but avoids useless recursion
                if not (prev_day < value[0] and min_stay <= value[0] - prev_day <= max_stay):
                    continue

            assignment[i] = value

            # Apply FC and remember what we deleted
            removed = forward_check(i)

            # If next domain isn't empty, continue search
            if i == K - 1 or domains[i + 1]:
                if backtrack(i + 1):
                    return True

            # Undo forward checking (manual rollback)
            # Tried deepcopy before — too slow and ugly
            domains[i + 1].extend(removed) if i < K - 1 else None
            assignment[i] = None

        return False

    # -----------------------------
    # Run solver
    # -----------------------------
    if backtrack(0):
        total_cost = 0
        for i in range(K):
            o = cities[i]
            d = cities[i + 1]
            day, price = assignment[i]
            total_cost += price
            print(f"{o} {d} {day} {price}")
        print(f"Total Cost: {total_cost}")
    else:
        print("No Solution")


if __name__ == "__main__":
    # Running from main avoids weird variable leaks when testing
    main()