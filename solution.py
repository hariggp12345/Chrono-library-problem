class ImprovedChronoOptimizer:
    def solve(self, time_limit, paradox_limit, books_data, connections):
        # Separate safe and risky books
        safe_books = []
        risky_books = []
        
        for book in books_data:
            book_id, value, stability, time = book
            if stability <= 3:
                risky_books.append((value / (time + 15), book))  # Value per paradox-minute
            else:
                safe_books.append((value / time, book))  # Value per minute
        
        # Sort both lists
        safe_books.sort(reverse=True)
        risky_books.sort(reverse=True)
        
        rescued = []
        total_time = 0
        total_value = 0
        paradoxes = 0
        
        # First take best safe books
        for score, book in safe_books:
            book_id, value, stability, time = book
            if total_time + time <= time_limit:
                rescued.append(book_id)
                total_value += value
                total_time += time
        
        # Then take best risky books (using paradox budget)
        for score, book in risky_books:
            if paradoxes >= paradox_limit:
                break
            book_id, value, stability, time = book
            time_cost = time + 15
            if total_time + time_cost <= time_limit:
                rescued.append(book_id)
                total_value += value
                total_time += time_cost
                paradoxes += 1
        
        return {
            "rescued_books": rescued,
            "total_value": total_value,
            "paradox_count": paradoxes,
            "time_used": total_time,
            "success": total_time <= time_limit and paradoxes <= paradox_limit
        }

def get_user_input():
    print("🏛️ CHRONO-LIBRARY RESCUE MISSION INPUT")
    print("=" * 50)
    
    # Get basic constraints
    time_limit = int(input("Enter time limit (minutes): "))
    paradox_limit = int(input("Enter paradox limit: "))
    
    # Get number of books
    num_books = int(input("Enter number of books: "))
    
    books_data = []
    print("\nEnter book details [id, value, stability, rescue_time]:")
    for i in range(num_books):
        while True:
            try:
                book_input = input(f"Book {i+1}: ")
                book_data = list(map(int, book_input.split(',')))
                if len(book_data) == 4:
                    books_data.append(book_data)
                    break
                else:
                    print("Please enter exactly 4 numbers separated by commas")
            except ValueError:
                print("Please enter valid numbers")
    
    # Get connections
    connections = []
    print("\nEnter shelf connections [id1, id2] (enter 'done' to finish):")
    while True:
        conn_input = input("Connection: ").strip()
        if conn_input.lower() == 'done':
            break
        try:
            conn_data = list(map(int, conn_input.split(',')))
            if len(conn_data) == 2:
                connections.append(conn_data)
            else:
                print("Please enter exactly 2 numbers separated by commas")
        except ValueError:
            print("Please enter valid numbers or 'done' to finish")
    
    return {
        "time_limit": time_limit,
        "paradox_limit": paradox_limit,
        "books": books_data,
        "connections": connections
    }

def main():
    # Get input from user
    input_data = get_user_input()
    
    # Solve the problem
    optimizer = ImprovedChronoOptimizer()
    result = optimizer.solve(
        input_data["time_limit"],
        input_data["paradox_limit"], 
        input_data["books"],
        input_data["connections"]
    )
    
    # Display results
    print("\n" + "=" * 50)
    print("🎯 RESCUE RESULTS")
    print("=" * 50)
    print(f"📚 Books rescued: {result['rescued_books']}")
    print(f"💰 Total value: {result['total_value']}")
    print(f"⚡ Paradoxes created: {result['paradox_count']}")
    print(f"⏰ Time used: {result['time_used']}/{input_data['time_limit']} minutes")
    print(f"✅ Mission status: {'SUCCESS' if result['success'] else 'FAILED'}")
    
    # Validate the solution
    print("\n📊 VALIDATION:")
    books_dict = {book[0]: book for book in input_data["books"]}
    total_time = 0
    calculated_value = 0
    calculated_paradoxes = 0
    
    for book_id in result['rescued_books']:
        book = books_dict[book_id]
        calculated_value += book[1]
        total_time += book[3]
        if book[2] <= 3:
            calculated_paradoxes += 1
            total_time += 15
    
    print(f"Calculated value: {calculated_value}")
    print(f"Calculated time: {total_time} minutes") 
    print(f"Calculated paradoxes: {calculated_paradoxes}")
    
    if (calculated_value == result['total_value'] and 
        total_time == result['time_used'] and 
        calculated_paradoxes == result['paradox_count']):
        print("✅ Solution is mathematically correct!")
    else:
        print("❌ Solution has calculation errors!")

if __name__ == "__main__":
    main()
