# Shopping API

Build a RESTful API for a part of a mini shopping app.

## Functional requirements

- Ability to create/remove/read products.
- Ability to calculate cart totals without placing an order.
- Rules for the cart calculation:
  - Every fifth product of same kind is free (order 6 cokes, pay only for 5...);
  - Total amount cannot exceed 100$;
  - Apply a 1$ discount when total amount is 20$ or more

## Technical requirements

- Build a RESTful API (you can choose the technology from Python, Node.js, Java, C# or Go)
- Pay attention to code structure, architecture and API design. Write the code so that it is easy to add more cart calculation rules in the future.
- Use any form of storage to save products & orders.
- Cover the solution with tests.
- Include README with clear instructions on how to build and run your solution.

## Bonus requirements

- Provide OpenAPI documentation
- Use functional programming principles where possible.
- Load cart calculation rules from external storage.
