from django.core.management.base import BaseCommand
from core.models import LLDProblem, ProblemRequirement
from core.domain.enums import Difficulty

class Command(BaseCommand):
    help = "Seeds database with comprehensive Low-Level Design problems, progressive requirements, and tags."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding LLD Problems..."))

        problems_data = [
            # 1. PARKING LOT SYSTEM
            {
                "slug": "parking-lot",
                "title": "Parking Lot System",
                "difficulty": Difficulty.MEDIUM.value,
                "estimated_time_minutes": 45,
                "tags": ["#StrategyPattern", "#FactoryPattern", "#ObserverPattern", "#Concurrency", "#MultiFloor"],
                "summary": "Design an automated multi-floor parking lot system supporting diverse vehicle types, automated ticketing, dynamic pricing, and intelligent spot allocation.",
                "problem_statement": """
### Problem Overview
A modern commercial complex requires a scalable, automated Parking Lot System. The parking facility spans multiple floors, accommodates various vehicle categories (Motorcycles, Cars, Vans, Trucks, and Electric Vehicles), and operates autonomous entry and exit gates.

The system must handle high concurrent traffic during peak hours, optimize spot allocation, track real-time occupancy across floors, compute flexible parking fees based on duration and vehicle type, and process multiple payment methods.

### Core Objectives
1. Model physical infrastructure (Floors, Spots, Gates, Display Boards).
2. Model vehicle classification and spot dimension compatibility.
3. Manage the end-to-end ticketing lifecycle from entry issue to exit validation and payment.
4. Support configurable spot allocation strategies (e.g. nearest to entry, lowest floor first).
5. Ensure extensibility for future pricing models, vehicle types, and payment processors.
""",
                "constraints": [
                    "Must support up to 5,000 parking spots across 10 floors with fast sub-second spot lookup.",
                    "Thread-safe spot reservation and ticket generation under concurrent entry requests.",
                    "Zero double-booking of spots when multiple gates attempt allocation simultaneously.",
                    "Graceful handling of full capacity and hardware/gate communication failures."
                ],
                "expected_design_considerations": [
                    "Apply Strategy Pattern for spot allocation algorithms and dynamic fee pricing.",
                    "Apply Factory Pattern for vehicle and spot instantiation.",
                    "Apply Observer Pattern for real-time floor display board and capacity updates.",
                    "Avoid God Object anti-pattern: Decompose ParkingLot facade into dedicated services (SpotAssignmentService, PaymentService, GateController).",
                    "Adhere strictly to Single Responsibility Principle (SRP) and Open/Closed Principle (OCP)."
                ],
                "hints": [
                    "Separate physical domain models (Floor, Spot, Gate) from transactional models (Ticket, PaymentTransaction, Receipt).",
                    "Introduce a ParkingSpotAllocationStrategy interface with implementations like NearestSpotStrategy and LowestFloorFirstStrategy.",
                    "Decouple payment processing via a PaymentProcessor interface (CardPaymentProcessor, CashPaymentProcessor, UPIPaymentProcessor)."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Multi-Vehicle Support",
                        "description": "Support multiple vehicle types: Motorcycle, Compact Car, Large SUV/Van, Heavy Truck, and Electric Vehicle.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Vehicle", "Motorcycle", "Car", "Truck", "ElectricVehicle", "VehicleType"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Spot Types & Sizing",
                        "description": "Provide dedicated spots: MotorcycleSpot, CompactSpot, LargeSpot, HandicappedSpot, and ElectricChargingSpot with occupancy status.",
                        "category": "CORE_ENTITY",
                        "keywords": ["ParkingSpot", "CompactSpot", "LargeSpot", "MotorcycleSpot", "ElectricSpot", "SpotStatus"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Multi-Floor Infrastructure",
                        "description": "Organize spots into multiple floors with real-time occupancy count and display indicators per floor.",
                        "category": "STRUCTURAL",
                        "keywords": ["Floor", "ParkingFloor", "DisplayBoard", "occupancy", "spots"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Entry & Exit Gate Operations",
                        "description": "Entry gates issue time-stamped barcode/RFID parking tickets. Exit gates validate tickets, trigger payment, and open barriers.",
                        "category": "FUNCTIONAL",
                        "keywords": ["EntryGate", "ExitGate", "Gate", "Ticket", "issueTicket", "validateTicket"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Dynamic Pricing & Payment Processing",
                        "description": "Compute parking fees based on vehicle type, stay duration, and peak pricing rules. Support Credit Card, Cash, and Digital Wallet payments.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Payment", "PricingStrategy", "PaymentProcessor", "FeeCalculator", "calculateFee", "processPayment"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Intelligent Spot Allocation Strategy",
                        "description": "Assign optimal available spot to incoming vehicles using pluggable allocation strategies (e.g. Nearest to Entrance, Lowest Floor).",
                        "category": "ALGORITHMIC",
                        "keywords": ["AllocationStrategy", "NearestSpotStrategy", "allocateSpot", "findSpot"],
                        "is_advanced": True,
                        "order": 6
                    },
                    {
                        "req_code": "REQ-7",
                        "title": "Real-time Display Board Observers",
                        "description": "Notify digital display boards on every entrance/floor immediately whenever a spot is occupied or vacated.",
                        "category": "BEHAVIORAL",
                        "keywords": ["DisplayBoard", "Observer", "notify", "updateOccupancy"],
                        "is_advanced": True,
                        "order": 7
                    }
                ]
            },

            # 2. ELEVATOR SYSTEM
            {
                "slug": "elevator-system",
                "title": "Elevator System",
                "difficulty": Difficulty.HARD.value,
                "estimated_time_minutes": 60,
                "tags": ["#StatePattern", "#CommandPattern", "#StrategyPattern", "#RealTime", "#Concurrency"],
                "summary": "Design a real-time multi-elevator scheduling and dispatching system for a high-rise building with complex motion states and optimization algorithms.",
                "problem_statement": """
### Problem Overview
A 50-story commercial skyscraper requires an intelligent Elevator Control System managing a bank of 8 synchronized elevator cars. The system coordinates passenger requests generated from floor hallway panels (external requests) and inside elevator car buttons (internal destinations).

The system must minimize average passenger wait times, optimize energy efficiency, prevent mechanical wear, handle peak-hour traffic surges (morning up-peak and evening down-peak), and manage emergency stop/fire alarm safety protocols.

### Core Objectives
1. Model the elevator car hierarchy, floor requests, door controllers, and weight sensors.
2. Model discrete motion states (IDLE, MOVING_UP, MOVING_DOWN, DOORS_OPENING, DOORS_OPEN, EMERGENCY_STOP).
3. Implement pluggable dispatching and scheduling algorithms (e.g., SCAN/Elevator algorithm, LOOK, Shortest Seek Time First, Zone Dispatching).
4. Maintain thread-safe scheduling under high-frequency asynchronous passenger requests.
""",
                "constraints": [
                    "Support up to 10 elevators serving 60 floors with sub-100ms dispatch decisions.",
                    "Enforce strict maximum capacity and overload weight sensor safety limits.",
                    "Elevators must never reverse direction with pending passengers inside travelling in the original direction.",
                    "Support fire alarms and emergency power cut-off states with immediate ground floor homing."
                ],
                "expected_design_considerations": [
                    "Apply State Pattern to model ElevatorCar motion and door transitions.",
                    "Apply Strategy Pattern for dispatch algorithms (SCANAlgorithm, LookAlgorithm, SectorDispatchStrategy).",
                    "Apply Command Pattern to encapsulate HallCall and DestinationCall requests into queueable command objects.",
                    "Use Observer Pattern to broadcast car arrival events to floor audio-visual chimes and hallway indicators."
                ],
                "hints": [
                    "Distinguish between an ExternalRequest (Origin floor + Up/Down direction) and an InternalRequest (Destination floor from inside car).",
                    "Maintain two separate priority queues or sorted sets per elevator: one for the current direction and one for the reverse direction.",
                    "Create an ElevatorController / Dispatcher service that aggregates hall calls and calculates the optimal car based on distance, direction, and load."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Elevator Car Modeling & State Machine",
                        "description": "Model ElevatorCar with current floor, direction, state (IDLE, MOVING_UP, MOVING_DOWN, DOORS_OPEN), capacity, and load weight.",
                        "category": "CORE_ENTITY",
                        "keywords": ["ElevatorCar", "ElevatorState", "Direction", "Door", "WeightSensor", "currentFloor"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Hallway Panel & In-Car Button Panels",
                        "description": "Handle external hall calls (source floor + UP/DOWN direction) and internal destination button selections.",
                        "category": "FUNCTIONAL",
                        "keywords": ["HallButton", "ElevatorButton", "ExternalRequest", "InternalRequest", "Request", "pressButton"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Central Dispatcher & Fleet Controller",
                        "description": "Coordinate fleet of elevator cars, assign external requests to optimal car, and route cars efficiently.",
                        "category": "STRUCTURAL",
                        "keywords": ["ElevatorController", "Dispatcher", "ElevatorBank", "assignRequest", "step"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Pluggable Scheduling Strategy (SCAN / LOOK)",
                        "description": "Implement elevator scheduling algorithms (e.g. SCAN / Elevator Algorithm) to serve pending requests in motion trajectory.",
                        "category": "ALGORITHMIC",
                        "keywords": ["SchedulingStrategy", "SCANStrategy", "LookStrategy", "getNextStop", "optimizeStops"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Overload & Emergency Safety Protocols",
                        "description": "Handle weight sensor overload alerts (prevent doors closing when overweight) and Fire Alarm emergency evacuation modes.",
                        "category": "BEHAVIORAL",
                        "keywords": ["EmergencyState", "OverloadException", "SafetyController", "triggerFireAlarm", "handleOverload"],
                        "is_advanced": True,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Zone-Based Traffic Optimization",
                        "description": "Support dynamic zoning during peak morning hours (dedicating specific elevators to low-rise, mid-rise, and high-rise zones).",
                        "category": "ALGORITHMIC",
                        "keywords": ["ZoneDispatchStrategy", "ZoningService", "TrafficPeakMode", "allocateZone"],
                        "is_advanced": True,
                        "order": 6
                    }
                ]
            },

            # 3. VENDING MACHINE SYSTEM
            {
                "slug": "vending-machine",
                "title": "Vending Machine System",
                "difficulty": Difficulty.EASY.value,
                "estimated_time_minutes": 30,
                "tags": ["#StatePattern", "#InventoryManagement", "#PaymentStrategy", "#ChangeCalculation"],
                "summary": "Design a reliable, state-driven vending machine handling product inventories, multi-denomination payments, coin change calculation, and transaction rollbacks.",
                "problem_statement": """
### Problem Overview
Design a modern automated snack and beverage Vending Machine. The machine supports item selection across multi-row inventory racks, accepts various payment methods (Coins, Banknotes, Contactless Cards), checks product inventory, dispenses selected items, and computes exact change using available cash reserves.

The system must handle failure scenarios gracefully (e.g., item out of stock, insufficient funds inserted, machine out of change coins, user cancels transaction mid-way) and maintain internal accounting records.

### Core Objectives
1. Model product catalog, item inventory slots, and cash denomination inventory.
2. Implement a strict State Pattern covering the transaction lifecycle:
   - `NoCoinState` (Idle / Ready)
   - `HasCoinState` (Coins inserted, awaiting selection or additional balance)
   - `SoldState` (Item dispensing in progress)
   - `DispenseChangeState` (Computing & returning change)
   - `OutOfStockState` / `MaintenanceState`
3. Implement an optimal coin change return algorithm using available denomination inventory.
4. Support transaction cancellation with 100% accurate full refund.
""",
                "constraints": [
                    "Machine must never dispense an item without receiving full payment.",
                    "If machine runs out of change coins to satisfy exact change, transaction must cancel and return inserted funds.",
                    "Inventory counts must decrement atomically upon successful physical dispense.",
                    "Support administrative restock and cash withdrawal operations."
                ],
                "expected_design_considerations": [
                    "Apply State Pattern to govern valid state transitions and prevent illegal operations (e.g. dispensing before paying).",
                    "Apply Strategy Pattern for payment processing (Coin/Cash, Card, Digital).",
                    "Decouple Physical Dispenser hardware interfaces from high-level vending transaction logic.",
                    "Adhere to SRP: Separate ItemInventoryManager, CashInventoryManager, and VendingMachineStateController."
                ],
                "hints": [
                    "Model Denomination as an Enum with monetary values (PENNY: 1, NICKEL: 5, DIME: 10, QUARTER: 25, DOLLAR: 100).",
                    "Maintain an internal CashInventory (map of Denomination to count) to verify whether exact change can be formed.",
                    "Every state class (e.g., HasMoneyState) should implement a common VendingMachineState interface."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Product Catalog & Rack Inventory Management",
                        "description": "Model Product (name, code, price) and InventorySlot (shelf rack, product, current count, max capacity).",
                        "category": "CORE_ENTITY",
                        "keywords": ["Product", "Inventory", "InventorySlot", "Rack", "Item", "getProduct", "deductStock"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "State Pattern Transaction Lifecycle",
                        "description": "Implement complete state transitions: IdleState, HasMoneyState, DispensingItemState, and DispensingChangeState.",
                        "category": "STRUCTURAL",
                        "keywords": ["VendingMachineState", "IdleState", "HasMoneyState", "DispenseState", "insertMoney", "selectProduct"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Multi-Denomination Cash & Payment Handling",
                        "description": "Accept coins and notes of various denominations, track accumulated session balance, and validate against item price.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Coin", "Note", "Denomination", "CashInventory", "insertedBalance", "acceptMoney"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Optimal Change Dispensing & Greedy Calculation",
                        "description": "Compute and dispense exact change using largest available denominations first; handle inability to return exact change.",
                        "category": "ALGORITHMIC",
                        "keywords": ["ChangeCalculator", "dispenseChange", "getChangeBreakdown", "insufficientChange"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Transaction Cancellation & Full Refund",
                        "description": "Allow user to cancel transaction prior to dispensing; refund 100% of inserted money and return to Idle state.",
                        "category": "FUNCTIONAL",
                        "keywords": ["cancelTransaction", "refund", "returnMoney", "abort"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Administrative Restock & Audit Logging",
                        "description": "Provide administrative interface for restocking products, replenishing change coins, and collecting accumulated cash revenue.",
                        "category": "BEHAVIORAL",
                        "keywords": ["AdminService", "restock", "collectCash", "AuditLogger"],
                        "is_advanced": True,
                        "order": 6
                    }
                ]
            },

            # 4. LIBRARY MANAGEMENT SYSTEM
            {
                "slug": "library-management-system",
                "title": "Library Management System",
                "difficulty": Difficulty.MEDIUM.value,
                "estimated_time_minutes": 45,
                "tags": ["#CatalogSearch", "#StrategyPattern", "#ReservationQueue", "#ObserverPattern", "#FineCalculator"],
                "summary": "Design an enterprise library management platform managing physical book copies, member borrowing limits, reservation waitlists, fine calculations, and notifications.",
                "problem_statement": """
### Problem Overview
A metropolitan university library requires a scalable, automated Library Management System. The library manages a large catalog of book titles, each having multiple physical barcoded copies (BookItems) distributed across various library branches and racks.

The system manages user accounts (Members, Librarians, Guests), borrowing policies (lending limits, checkout duration), reservation queues for loaned items, overdue fine calculations, and automated notification alerts.

### Core Objectives
1. Decouple abstract bibliographic metadata (`Book`) from physical shelf copies (`BookItem` with barcode, RFID tag, and shelf location).
2. Manage member borrowing lifecycles (Checkout, Renewal, Return, Lost declaration) enforcing borrowing quotas per membership tier.
3. Manage FIFO reservation queues for books currently on loan.
4. Support flexible overdue fine calculation strategies and fee collection.
5. Provide a multi-criteria search catalog supporting lookup by Title, Author, Subject, ISBN, and Publication Year.
""",
                "constraints": [
                    "Members cannot exceed their maximum allowable active loan quota (e.g. 5 books for Students, 10 for Faculty).",
                    "A reserved book cannot be checked out by another member when returned; it must be held for the reserving member for 48 hours.",
                    "Fine accrual must calculate daily according to member tier and days overdue.",
                    "Thread-safe checkout and reservation operations to prevent race conditions on the last available copy."
                ],
                "expected_design_considerations": [
                    "Apply Separate Metadata from Physical Item pattern (Book vs BookItem).",
                    "Apply Strategy Pattern for fine calculation (StudentFineStrategy, FacultyFineStrategy).",
                    "Apply Observer Pattern to dispatch email/SMS alerts when a reserved book becomes available or a loan is overdue.",
                    "Apply State Pattern for BookItem status (AVAILABLE, LOANED, RESERVED, LOST, DAMAGED)."
                ],
                "hints": [
                    "Do not put physical properties like barcode, rackNumber, or status in the Book class. Those belong in BookItem.",
                    "Create a LendingTransaction or BookLending record linking a Member, BookItem, issueDate, dueDate, and returnDate.",
                    "Model the Reservation Queue as a FIFO waitlist per Book."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Book vs BookItem Separation",
                        "description": "Differentiate abstract bibliographic Book (ISBN, Title, Authors, Subject) from physical BookItem (barcode, rackNumber, status, price).",
                        "category": "CORE_ENTITY",
                        "keywords": ["Book", "BookItem", "BookStatus", "Barcode", "Author", "ISBN"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Member & Librarian Hierarchy",
                        "description": "Support Member accounts (Student, Faculty) with max loan limits and Librarian administrative accounts.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Account", "Member", "Librarian", "StudentMember", "FacultyMember", "maxQuota"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Book Checkout & Return Lifecycle",
                        "description": "Process book issue and return transactions; update copy status and track issue date, due date, and return timestamp.",
                        "category": "FUNCTIONAL",
                        "keywords": ["BookLending", "checkout", "returnBook", "renewBook", "dueDate"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "FIFO Book Reservation Queue",
                        "description": "Allow members to reserve checked-out books. When returned, place copy on hold for next member in reservation queue.",
                        "category": "FUNCTIONAL",
                        "keywords": ["BookReservation", "ReservationQueue", "reserveBook", "cancelReservation", "holdBook"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Configurable Fine Calculation & Settlement",
                        "description": "Calculate daily late return penalties according to member tier and overdue days. Support fine settlement transactions.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Fine", "FineCalculator", "FineStrategy", "calculateFine", "payFine"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Multi-Criteria Catalog Search Engine",
                        "description": "Enable efficient search of catalog items by title keywords, author name, subject category, and publication year.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Catalog", "SearchEngine", "SearchStrategy", "searchByTitle", "searchByAuthor"],
                        "is_advanced": True,
                        "order": 6
                    },
                    {
                        "req_code": "REQ-7",
                        "title": "Notification Dispatcher Service",
                        "description": "Dispatch automated Email/SMS notifications for due date reminders, reservation readiness, and overdue alerts.",
                        "category": "BEHAVIORAL",
                        "keywords": ["NotificationService", "Notification", "Observer", "sendDueDateReminder"],
                        "is_advanced": True,
                        "order": 7
                    }
                ]
            },

            # 5. SPLITWISE (EXPENSE SHARING APPLICATION)
            {
                "slug": "splitwise",
                "title": "Splitwise (Expense Sharing System)",
                "difficulty": Difficulty.MEDIUM.value,
                "estimated_time_minutes": 45,
                "tags": ["#StrategyPattern", "#ObserverPattern", "#DebtSimplification", "#CompositePattern", "#BalanceSheet"],
                "summary": "Design an expense sharing platform allowing users to form groups, add expenses with flexible split strategies (Equal, Exact, Percentage), manage balance sheets, and simplify group debts.",
                "problem_statement": """
### Problem Overview
Design a collaborative Expense Sharing application like Splitwise. The platform enables users to register, create groups (e.g. Roommates, Trip to Europe), record multi-party expenses, allocate splits among participants, track individual balance sheets, and settle debts efficiently.

The system must handle diverse split distributions (Equal split, Exact amount split, Percentage split, and Share-based split), ensure fractional currency balance invariants, and provide an algorithm to simplify group debts to minimize the total number of cash settlement transactions.

### Core Objectives
1. Model User profiles, Groups, Expenses, and participant Splits.
2. Implement Strategy Pattern for pluggable split calculation strategies (EqualSplit, ExactSplit, PercentageSplit).
3. Maintain pairwise balances and individual user balance sheets in real time.
4. Implement a Debt Simplification graph algorithm that minimizes cash transfer transactions across a group.
5. Provide direct settlement transactions to clear balances between pairs of users.
""",
                "constraints": [
                    "Sum of all participant split shares must strictly equal the total expense amount (handling 1-cent/paisa rounding errors).",
                    "Percentage splits must sum to exactly 100%.",
                    "Zero sum balance sheet invariant: Across the whole system or closed group, total money owed equals total money to be received.",
                    "Support concurrent expense entries in large active groups."
                ],
                "expected_design_considerations": [
                    "Apply Strategy Pattern for Split calculation algorithms (EqualSplitStrategy, ExactSplitStrategy, PercentageSplitStrategy).",
                    "Apply Observer Pattern to notify group participants whenever an expense is added, edited, or settled.",
                    "Apply Factory Pattern for creating Expense and Split entities based on ExpenseType.",
                    "Decouple balance sheet computation from entity storage (BalanceSheetManager, DebtSimplificationService)."
                ],
                "hints": [
                    "Model each participant's share in an expense as a Split entity containing user and amount.",
                    "Maintain a balance map: `Map<User, Map<User, Double>>` representing pairwise net balances.",
                    "For Debt Simplification: compute net balance per user, sort into creditors (+ve) and debtors (-ve), and use a two-pointer greedy match to minimize transaction count."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "User Profile & Group Management",
                        "description": "Model User accounts (id, name, email, phone) and Groups with multiple participant members.",
                        "category": "CORE_ENTITY",
                        "keywords": ["User", "Group", "Member", "createGroup", "addMember"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Expense Modeling & Multi-Payer Support",
                        "description": "Record expenses with title, total amount, paid-by user(s), expense date, category, and group context.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Expense", "ExpenseType", "PaidBy", "TotalAmount", "addExpense"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Pluggable Split Calculation Strategies",
                        "description": "Support Equal, Exact, Percentage, and Share split strategies; validate that split sums equal the total expense amount.",
                        "category": "ALGORITHMIC",
                        "keywords": ["SplitStrategy", "EqualSplitStrategy", "ExactSplitStrategy", "PercentageSplitStrategy", "calculateSplits", "validateSplit"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Real-Time User & Group Balance Sheets",
                        "description": "Compute pairwise balances (User A owes User B $25) and overall user net balance sheets in real time.",
                        "category": "FUNCTIONAL",
                        "keywords": ["BalanceSheet", "UserBalance", "getUserBalances", "getGroupBalances", "updateBalances"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Direct Settlement & Payment Recording",
                        "description": "Record settlement payments between two users to clear or reduce outstanding debt balances.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Settlement", "PaymentTransaction", "settleUp", "recordPayment"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Group Debt Simplification Engine",
                        "description": "Apply a min-cash-flow graph algorithm to consolidate transitive debts in a group into minimum number of transactions.",
                        "category": "ALGORITHMIC",
                        "keywords": ["DebtSimplificationService", "simplifyDebts", "minimizeCashFlow", "NetBalance"],
                        "is_advanced": True,
                        "order": 6
                    },
                    {
                        "req_code": "REQ-7",
                        "title": "Activity History & Notification Observers",
                        "description": "Maintain audit activity logs of all financial events and dispatch notifications to involved members on new expenses.",
                        "category": "BEHAVIORAL",
                        "keywords": ["ActivityLog", "NotificationService", "Observer", "notifyMembers"],
                        "is_advanced": True,
                        "order": 7
                    }
                ]
            },

            # 6. BOOKMYSHOW (MOVIE TICKET BOOKING SYSTEM)
            {
                "slug": "bookmyshow",
                "title": "Movie Ticket Booking (BookMyShow)",
                "difficulty": Difficulty.HARD.value,
                "estimated_time_minutes": 60,
                "tags": ["#Concurrency", "#DistributedLocking", "#ObserverPattern", "#StrategyPattern", "#StatePattern"],
                "summary": "Design a high-concurrency movie ticket booking platform supporting cinemas, multi-tier seat layouts, temporary seat locking with TTL, dynamic pricing, and payment confirmation.",
                "problem_statement": """
### Problem Overview
Design an online Movie Ticket Booking platform like BookMyShow. The system spans multi-city cinema complexes, auditoriums with tiered seating (Silver, Gold, Platinum, Recliner), movie catalogs, and scheduled showtimes.

During high-demand blockbuster ticket releases, thousands of users select seats simultaneously. The system must prevent double-booking, lock chosen seats temporarily for 10 minutes while the user completes payment, release expired locks automatically, process payments, and issue QR-coded digital tickets.

### Core Objectives
1. Model physical Cinema complexes, Screens/Halls, and Tiered Seating arrangements.
2. Model Movies, Shows, and ShowSeat inventory with real-time seat availability maps.
3. Implement a thread-safe Temporary Seat Locking mechanism with TTL expiration.
4. Support dynamic seat pricing strategies (weekend surcharges, matinee discounts, tier multipliers).
5. Manage complete Booking lifecycle from seat selection to payment settlement and ticket dispatch.
""",
                "constraints": [
                    "Zero double-booking under extreme concurrent requests for the same seats.",
                    "Temporary seat lock must automatically expire after 10 minutes if payment is not confirmed.",
                    "Sub-second movie and show search by city, genre, language, and format (2D, 3D, IMAX).",
                    "Atomic payment confirmation and seat status update."
                ],
                "expected_design_considerations": [
                    "Apply State Pattern for ShowSeat status (AVAILABLE, TEMPORARILY_LOCKED, BOOKED, BLOCKED).",
                    "Apply Strategy Pattern for Dynamic Pricing (StandardPricingStrategy, WeekendSurgeStrategy, TierPricingStrategy).",
                    "Apply Observer Pattern for Booking notifications and seat lock expiration listeners.",
                    "Separate static physical theater models (Cinema, Screen, Seat) from transactional models (Show, ShowSeat, Booking, Payment)."
                ],
                "hints": [
                    "Distinguish between physical Seat (static template in a screen) and ShowSeat (created per Show with dynamic price and status).",
                    "Introduce a SeatLockService that maps showSeat IDs to lock timestamps and user IDs.",
                    "Create a Booking entity that references locked ShowSeats and has states (PENDING_PAYMENT, CONFIRMED, EXPIRED, CANCELLED)."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Cinema, Screen & Tiered Seating Infrastructure",
                        "description": "Model Cinema complexes across cities, individual Screens/Halls, and physical Seats with tiers (Silver, Gold, Platinum).",
                        "category": "CORE_ENTITY",
                        "keywords": ["Cinema", "Screen", "Seat", "SeatType", "City", "Auditorium"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Movie Catalog & Scheduled Shows",
                        "description": "Manage Movie listings (title, duration, genre, language) and scheduled Show instances in specific screens.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Movie", "Show", "Schedule", "startTime", "endTime", "MovieSearch"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Show Seat Inventory & Real-Time Layout",
                        "description": "Provide real-time seat availability matrix for a show; differentiate available, locked, and booked seats.",
                        "category": "STRUCTURAL",
                        "keywords": ["ShowSeat", "SeatStatus", "getAvailableSeats", "getSeatMap"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Temporary Seat Locking with Expiration TTL",
                        "description": "Lock selected seats atomically for 10 minutes during checkout; automatically release seats if checkout is abandoned.",
                        "category": "ALGORITHMIC",
                        "keywords": ["SeatLockManager", "lockSeats", "unlockExpiredSeats", "isSeatLocked", "lockTimeout"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Booking Lifecycle & Payment Confirmation",
                        "description": "Process booking creation, integrate payment processing, transition locked seats to BOOKED, and issue confirmed tickets.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Booking", "BookingStatus", "PaymentService", "createBooking", "confirmBooking"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Dynamic Pricing & Seat Tier Multipliers",
                        "description": "Calculate dynamic ticket prices based on seat tier, showtime (morning vs evening), and weekend surge factors.",
                        "category": "ALGORITHMIC",
                        "keywords": ["PricingStrategy", "DynamicPricing", "calculateSeatPrice", "WeekendSurgeStrategy"],
                        "is_advanced": True,
                        "order": 6
                    },
                    {
                        "req_code": "REQ-7",
                        "title": "Booking Cancellation & Automated Refund",
                        "description": "Allow users to cancel bookings within allowable cancellation windows; process refunds and mark seats available.",
                        "category": "FUNCTIONAL",
                        "keywords": ["cancelBooking", "RefundService", "processRefund", "releaseBookedSeats"],
                        "is_advanced": True,
                        "order": 7
                    }
                ]
            },

            # 7. SNAKE AND LADDER (BOARD GAME ENGINE)
            {
                "slug": "snake-and-ladder",
                "title": "Snake and Ladder Game",
                "difficulty": Difficulty.EASY.value,
                "estimated_time_minutes": 30,
                "tags": ["#StrategyPattern", "#FactoryPattern", "#GameState", "#BoardGameEngine", "#ExtensibleBoard"],
                "summary": "Design an extensible Snake and Ladder board game engine supporting configurable grid sizes, arbitrary snakes and ladders, customizable dice rolling strategies, and multiple players.",
                "problem_statement": """
### Problem Overview
Design a modular object-oriented Snake and Ladder Board Game engine. The game supports a customizable board of $N$ cells (standard 100 cells), configurable placements of Snakes (moving players downward) and Ladders (elevating players upward), multiple players, and customizable dice.

The engine must enforce strict game rules: players take turns rolling dice, land on obstacle cells, take jumps, and win by reaching the final winning cell with an exact dice roll.

### Core Objectives
1. Model Board, Cell, and polymorphic Jump obstacles (Snakes and Ladders).
2. Model Players, Game tokens, and turn rotation queues.
3. Apply Strategy Pattern for Dice rolling algorithms (Single standard 6-sided dice, Multiple dice, Crooked/Biased dice).
4. Implement GameController managing game states (NOT_STARTED, IN_PROGRESS, FINISHED) and evaluating win conditions.
""",
                "constraints": [
                    "A snake's head must strictly be at a higher cell number than its tail (Head > Tail).",
                    "A ladder's bottom must strictly be at a lower cell number than its top (Top > Bottom).",
                    "Prevent circular jump loops (e.g. Ladder pointing to Snake head pointing back to Ladder).",
                    "Player must roll the exact number required to land on the final winning cell (Cell 100)."
                ],
                "expected_design_considerations": [
                    "Apply Strategy Pattern for Dice rolling strategies (StandardDiceStrategy, CrookedDiceStrategy).",
                    "Abstract Snakes, Ladders, and future obstacles as polymorphic Jump / BoardEntity objects.",
                    "Use a FIFO Queue for fair player turn management in GameController.",
                    "Adhere to SRP: Separate Board, Dice, Player, and GameEngine responsibilities."
                ],
                "hints": [
                    "Model Jump as a base class or interface with startPosition and endPosition; Snake and Ladder inherit from Jump.",
                    "Maintain a `Map<Integer, Jump>` on the Board for $O(1)$ lookup when a player lands on a cell.",
                    "Use `Queue<Player>` in GameController: dequeue current player, roll dice, compute next position, apply jump, check win, and re-enqueue if not won."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Configurable Board & Coordinate Grid",
                        "description": "Model Board containing $N$ cells (default 100) with coordinate mapping and cell entity lookup.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Board", "Cell", "boardSize", "getCell", "initializeBoard"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Polymorphic Jump Entities (Snakes & Ladders)",
                        "description": "Model Jump base class with Snake (head > tail) and Ladder (top > bottom) specializations and position validation.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Jump", "Snake", "Ladder", "startPosition", "endPosition", "getEndPosition"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Pluggable Dice Rolling Strategy",
                        "description": "Implement pluggable Dice rolling strategies supporting standard 1-6 dice, multiple dice, and custom crooked dice.",
                        "category": "ALGORITHMIC",
                        "keywords": ["Dice", "DiceStrategy", "StandardDiceStrategy", "rollDice", "diceCount"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Player Management & Turn Execution Queue",
                        "description": "Manage player roster with unique IDs/tokens and rotate turns using a fair FIFO queue in the game engine.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Player", "GameController", "PlayerQueue", "takeTurn", "makeMove"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Win Condition & Exact Landing Rule",
                        "description": "Detect game victory when a player lands exactly on the final cell; skip moves that overshoot the board boundary.",
                        "category": "FUNCTIONAL",
                        "keywords": ["isWinner", "validateLanding", "winningPosition", "GameStatus"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Extensible Board Obstacles (Portals & Mines)",
                        "description": "Extend board obstacle framework to support new interactive entities like Portals (teleport) and Mines (skip turn).",
                        "category": "STRUCTURAL",
                        "keywords": ["Portal", "Mine", "BoardEntity", "applyObstacleEffect"],
                        "is_advanced": True,
                        "order": 6
                    }
                ]
            },

            # 8. AUTOMATED TELLER MACHINE (ATM SYSTEM)
            {
                "slug": "atm-system",
                "title": "Automated Teller Machine (ATM)",
                "difficulty": Difficulty.MEDIUM.value,
                "estimated_time_minutes": 45,
                "tags": ["#StatePattern", "#ChainOfResponsibility", "#TransactionManagement", "#HardwareAbstraction"],
                "summary": "Design a robust, secure ATM system orchestrating card insertion, PIN authentication, account balance inquiry, cash withdrawal via denomination handlers, and state management.",
                "problem_statement": """
### Problem Overview
Design a software architecture for an Automated Teller Machine (ATM) banking kiosk. The ATM coordinates physical hardware peripherals (Card Reader, Cash Dispenser, Keypad, Screen, Cash Deposit Slot, Receipt Printer), user interaction states, and secure communication with the Bank Core Banking System.

The system must handle customer authentication, cash withdrawals with optimal denomination note dispensing ($100, $50, $20, $10), account balance inquiries, cash deposits, PIN retry limits, and transaction rollbacks on hardware/network failures.

### Core Objectives
1. Implement a complete State Pattern governing ATM user session states:
   - `IdleState` (Awaiting card insertion)
   - `HasCardState` (Card inserted, awaiting PIN entry)
   - `AuthenticatedState` (PIN validated, awaiting transaction selection)
   - `DispensingCashState` (Dispensing physical cash notes)
2. Implement Chain of Responsibility Pattern for cash dispensing across available note denominations.
3. Manage secure PIN validation with a maximum 3-strike lockout policy.
4. Support polymorphic transaction commands (Withdrawal, Deposit, Balance Inquiry, PIN Change).
""",
                "constraints": [
                    "ATM must never dispense cash if total amount exceeds available account balance or daily withdrawal limits.",
                    "Accurately dispense cash notes using available physical cash inventory; fail transaction if exact combination cannot be formed.",
                    "Eject card immediately upon user cancellation or successful session termination.",
                    "Atomic transaction rollback if cash dispenser mechanism jams or fails."
                ],
                "expected_design_considerations": [
                    "Apply State Pattern to model ATM hardware and session transitions.",
                    "Apply Chain of Responsibility Pattern for Cash Dispensing ($100 -> $50 -> $20 -> $10 note handlers).",
                    "Apply Command Pattern to encapsulate banking transactions (WithdrawalTransaction, DepositTransaction, BalanceInquiryTransaction).",
                    "Decouple ATM controller from Core Banking Service using an Adapter interface."
                ],
                "hints": [
                    "Define an `ATMState` interface with operations: `insertCard`, `enterPin`, `selectTransaction`, `withdrawCash`, `ejectCard`.",
                    "Create a `CashDispenserChain` where each handler checks its available count of a specific denomination and delegates the remainder.",
                    "Separate `BankServiceAdapter` so the ATM logic does not know bank database internals."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "ATM Hardware & Cash Inventory",
                        "description": "Model ATM hardware components (CardReader, Keypad, CashDispenser, Screen) and physical cash note inventory counts.",
                        "category": "CORE_ENTITY",
                        "keywords": ["ATM", "CashInventory", "CashDispenser", "CardReader", "Denomination", "NoteCount"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "State Pattern ATM Session Lifecycle",
                        "description": "Implement State Pattern covering IdleState, HasCardState, AuthenticatedState, and DispensingState transitions.",
                        "category": "STRUCTURAL",
                        "keywords": ["ATMState", "IdleState", "HasCardState", "AuthenticatedState", "insertCard", "ejectCard"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Card Authentication & Security Strike Limit",
                        "description": "Verify card validity and customer PIN with the bank system; lock card after 3 consecutive failed PIN attempts.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Card", "Account", "authenticatePin", "strikeCount", "lockCard", "PINValidator"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Chain of Responsibility Cash Dispensing",
                        "description": "Dispense requested cash amount using Chain of Responsibility ($100 -> $50 -> $20 -> $10 note handlers); verify inventory.",
                        "category": "ALGORITHMIC",
                        "keywords": ["CashDispenseChain", "HundredDollarDispenser", "FiftyDollarDispenser", "dispenseCash", "validateInventory"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Polymorphic Banking Transactions",
                        "description": "Support Withdrawal, Cash Deposit, Balance Inquiry, and Mini-Statement transaction operations.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Transaction", "WithdrawalTransaction", "DepositTransaction", "BalanceInquiry", "executeTransaction"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Bank Gateway Adapter & Transaction Rollback",
                        "description": "Decouple ATM from core banking APIs using BankServiceAdapter; execute atomic transaction rollbacks on hardware faults.",
                        "category": "STRUCTURAL",
                        "keywords": ["BankServiceAdapter", "CoreBankGateway", "rollbackTransaction", "ReceiptPrinter"],
                        "is_advanced": True,
                        "order": 6
                    }
                ]
            },

            # 9. RATE LIMITER & API THROTTLING LIBRARY
            {
                "slug": "rate-limiter",
                "title": "Rate Limiter Library",
                "difficulty": Difficulty.HARD.value,
                "estimated_time_minutes": 60,
                "tags": ["#StrategyPattern", "#SlidingWindow", "#TokenBucket", "#Concurrency", "#ThreadSafety"],
                "summary": "Design a high-performance, thread-safe rate limiter middleware library supporting multiple throttling algorithms (Token Bucket, Leaky Bucket, Sliding Window Counter) and multi-tier client quotas.",
                "problem_statement": """
### Problem Overview
Design a reusable, high-performance Rate Limiter library to protect backend microservices from DDoS attacks, API abuse, and resource starvation. The library intercepts incoming requests, identifies clients by IP address, User ID, or API Key, and determines whether to allow or throttle the request according to configured rate limits.

The library must support pluggable rate limiting algorithms (Token Bucket, Leaky Bucket, Sliding Window Log, Sliding Window Counter), multi-tier client configurations (Free Tier: 10 req/min, Pro Tier: 1,000 req/min), thread-safe concurrency, and minimal latency overhead.

### Core Objectives
1. Implement a pluggable `RateLimiter` interface with method `boolean allowRequest(String clientId)`.
2. Implement multiple classic rate-limiting algorithms:
   - **Token Bucket**: Refill tokens dynamically based on time elapsed without background cron threads.
   - **Sliding Window Counter**: Smooth throttling across window boundaries.
   - **Leaky Bucket**: Enforce smooth output processing rates.
3. Manage multi-tier client rate limit policies (Free, Premium, Enterprise).
4. Maintain thread safety under high concurrent traffic using mutexes or atomic operations.
5. Provide automatic memory eviction of idle client buckets.
""",
                "constraints": [
                    "Sub-millisecond latency overhead (<1ms) per request evaluation.",
                    "Thread-safe token consumption under thousands of concurrent incoming HTTP requests.",
                    "Zero background thread leaks: Compute token refills on-demand using timestamp deltas.",
                    "Support standard HTTP rate limiting response headers (X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After)."
                ],
                "expected_design_considerations": [
                    "Apply Strategy Pattern for rate limiting algorithms (TokenBucketStrategy, SlidingWindowStrategy, LeakyBucketStrategy).",
                    "Apply Factory Pattern for creating rate limiters configured per client tier (RateLimiterFactory).",
                    "Decouple rate limiting core domain from storage backends (InMemoryStorageAdapter vs RedisStorageAdapter).",
                    "Ensure thread safety via ConcurrentHashMap, ReentrantLocks, or AtomicInteger counters."
                ],
                "hints": [
                    "For Token Bucket: Do not run a timer to add tokens. When a request arrives, calculate tokens to add: `(currentTime - lastRefillTime) * refillRatePerSecond`.",
                    "Store `ClientRateLimitConfig` per client tier containing capacity, refillRate, and timeUnit.",
                    "Wrap the rate limiter as an HTTP Middleware Interceptor."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "Rate Limiter Strategy Interface Contract",
                        "description": "Define abstract RateLimiter interface with allowRequest(clientId) and return RateLimitResult (isAllowed, remainingTokens, retryAfter).",
                        "category": "STRUCTURAL",
                        "keywords": ["RateLimiter", "RateLimiterStrategy", "RateLimitResult", "allowRequest", "clientId"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Token Bucket Algorithm Implementation",
                        "description": "Implement Token Bucket algorithm with lazy timestamp-based token refills, capacity limits, and token deduction.",
                        "category": "ALGORITHMIC",
                        "keywords": ["TokenBucketRateLimiter", "refillTokens", "capacity", "refillRate", "consumeToken"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Sliding Window Counter Algorithm",
                        "description": "Implement Sliding Window Counter algorithm weighing previous window request counts with current window progress.",
                        "category": "ALGORITHMIC",
                        "keywords": ["SlidingWindowCounterLimiter", "timeWindowSeconds", "maxRequests", "calculateWindowWeight"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Client Identification & Tiered Rate Limit Policies",
                        "description": "Support client identification (by IP, API Key, User ID) and map clients to tiered rate limit quotas (Free, Pro, Enterprise).",
                        "category": "FUNCTIONAL",
                        "keywords": ["ClientTier", "RateLimitConfig", "ClientIdentifier", "getLimitForClient", "TierPolicy"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Thread-Safe Concurrency & Atomic Execution",
                        "description": "Ensure thread-safe bucket updates under concurrent requests using atomic operations or fine-grained locks.",
                        "category": "STRUCTURAL",
                        "keywords": ["ConcurrentMap", "AtomicInteger", "ReentrantLock", "synchronizedExecution", "ThreadSafety"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Memory Eviction of Idle Client Buckets",
                        "description": "Implement an LRU or TTL-based eviction policy to purge client buckets that have had no traffic for a configurable duration.",
                        "category": "ALGORITHMIC",
                        "keywords": ["BucketEvictionManager", "evictIdleBuckets", "TTL", "LRUCache"],
                        "is_advanced": True,
                        "order": 6
                    },
                    {
                        "req_code": "REQ-7",
                        "title": "HTTP Middleware Interceptor & Response Headers",
                        "description": "Package rate limiter as a reusable HTTP middleware interceptor that attaches X-RateLimit-Limit and Retry-After headers.",
                        "category": "BEHAVIORAL",
                        "keywords": ["RateLimitMiddleware", "interceptRequest", "XRateLimitHeaders", "HTTP429TooManyRequests"],
                        "is_advanced": True,
                        "order": 7
                    }
                ]
            },

            # 10. CHESS GAME ENGINE
            {
                "slug": "chess-game",
                "title": "Chess Game Engine",
                "difficulty": Difficulty.HARD.value,
                "estimated_time_minutes": 60,
                "tags": ["#Polymorphism", "#StrategyPattern", "#CommandPattern", "#BoardGameEngine", "#MoveValidation"],
                "summary": "Design an object-oriented Chess game engine with an 8x8 board, polymorphic piece movement rules (King, Queen, Rook, Bishop, Knight, Pawn), move validation, check/checkmate detection, and turn management.",
                "problem_statement": """
### Problem Overview
Design a complete object-oriented Chess Game Engine conforming to standard FIDE chess rules. The system models an 8x8 board of 64 squares, two players (White and Black) each controlling 16 pieces (1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, 8 Pawns), turn alternation, legal move validation, move history, and checkmate evaluation.

The engine must enforce distinct movement rules for every piece type, validate that moves do not leave the friendly King in check, support special moves (Castling, En Passant, Pawn Promotion), and detect endgame states (Checkmate, Stalemate, Resignation).

### Core Objectives
1. Model Board, 64 Cells (Coordinates $A1$ to $H8$), and polymorphic Piece hierarchy.
2. Implement polymorphic move validation logic for King, Queen, Rook, Bishop, Knight, and Pawn.
3. Validate move legality: Path clearance for sliding pieces (Rook, Bishop, Queen), non-attacking friendly fire, and King safety.
4. Implement Check, Checkmate, and Stalemate detection engines.
5. Apply Command Pattern for Move execution and move history undo/redo.
""",
                "constraints": [
                    "A player can never make a move that leaves their own King in Check.",
                    "Path between start and destination cells must be clear of obstacles for sliding pieces (Rook, Bishop, Queen).",
                    "Pawns move forward 1 square (or 2 from start row) but capture diagonally 1 square.",
                    "Support algebraic chess notation logging (e.g., e4, Nf3, O-O)."
                ],
                "expected_design_considerations": [
                    "Abstract base class `Piece` with polymorphic `boolean canMove(Board board, Cell start, Cell end)`.",
                    "Apply Command Pattern for `Move` execution and history undo/redo (`makeMove`, `undoMove`).",
                    "Decouple `Board` grid and `Cell` representation from `GameController` orchestration and `Player` actors.",
                    "Separate `CheckDetector` and `MoveValidator` to keep class cohesion high."
                ],
                "hints": [
                    "Model Piece with attributes: `Color color`, `boolean isKilled`, `boolean hasMoved` and abstract `canMove()`.",
                    "Model Cell with `int row`, `int col`, and optional `Piece piece`.",
                    "To test if a move is legal: temporarily apply the move on the board, check if the friendly King is attacked, and rollback if invalid."
                ],
                "requirements": [
                    {
                        "req_code": "REQ-1",
                        "title": "8x8 Board & Cell Coordinate Grid",
                        "description": "Model 8x8 Board with 64 Cells, coordinate indexing (A1 to H8), piece placement, and initial board setup.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Board", "Cell", "initializeBoard", "getCell", "Color", "Coordinate"],
                        "is_advanced": False,
                        "order": 1
                    },
                    {
                        "req_code": "REQ-2",
                        "title": "Polymorphic Piece Hierarchy & Movement Rules",
                        "description": "Implement Piece abstract base class with polymorphic King, Queen, Rook, Bishop, Knight, and Pawn canMove rules.",
                        "category": "CORE_ENTITY",
                        "keywords": ["Piece", "King", "Queen", "Rook", "Bishop", "Knight", "Pawn", "canMove", "isValidMovePath"],
                        "is_advanced": False,
                        "order": 2
                    },
                    {
                        "req_code": "REQ-3",
                        "title": "Move Validation & Execution Engine",
                        "description": "Validate move legality, check path obstacles, prevent friendly capture, execute captures, and update piece position.",
                        "category": "FUNCTIONAL",
                        "keywords": ["Move", "MoveValidator", "executeMove", "isPathClear", "isFriendlyPiece"],
                        "is_advanced": False,
                        "order": 3
                    },
                    {
                        "req_code": "REQ-4",
                        "title": "Player Turn Alternation & Game Lifecycle",
                        "description": "Manage White and Black player turns, clock timers, and game states (ACTIVE, CHECK, CHECKMATE, STALEMATE, RESIGNED).",
                        "category": "FUNCTIONAL",
                        "keywords": ["Player", "GameController", "switchTurn", "GameStatus", "currentTurnPlayer"],
                        "is_advanced": False,
                        "order": 4
                    },
                    {
                        "req_code": "REQ-5",
                        "title": "Check, Checkmate & Stalemate Detection",
                        "description": "Detect whether a King is under check; determine checkmate (no legal escaping moves) and stalemate (no legal moves while not in check).",
                        "category": "ALGORITHMIC",
                        "keywords": ["CheckDetector", "isKingInCheck", "isCheckmate", "isStalemate", "hasLegalMoves"],
                        "is_advanced": False,
                        "order": 5
                    },
                    {
                        "req_code": "REQ-6",
                        "title": "Special Moves: Castling, En Passant & Pawn Promotion",
                        "description": "Support special chess moves: Kingside/Queenside Castling, En Passant pawn captures, and Pawn Promotion to Queen/Rook/Bishop/Knight.",
                        "category": "ALGORITHMIC",
                        "keywords": ["CastlingMove", "EnPassantMove", "PawnPromotion", "promotePawn", "canCastle"],
                        "is_advanced": True,
                        "order": 6
                    },
                    {
                        "req_code": "REQ-7",
                        "title": "Command-Pattern Move History & Undo/Redo",
                        "description": "Maintain move history log using Command Pattern; support move undo and redo with board state restoration.",
                        "category": "STRUCTURAL",
                        "keywords": ["MoveHistory", "undoMove", "redoMove", "MoveCommand", "AlgebraicNotation"],
                        "is_advanced": True,
                        "order": 7
                    }
                ]
            }
        ]

        for p_data in problems_data:
            reqs = p_data.pop("requirements")
            problem, created = LLDProblem.objects.update_or_create(
                slug=p_data["slug"],
                defaults=p_data
            )
            action_str = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"  [+] {action_str} problem: {problem.title}"))

            for r_data in reqs:
                ProblemRequirement.objects.update_or_create(
                    problem=problem,
                    req_code=r_data["req_code"],
                    defaults=r_data
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(problems_data)} comprehensive LLD problems with progressive requirements and tags!"))
