
## Online ticketing system for a fictive airline



## Requirements

• There exist two types of users for the system; company employees and clients. For their identification, the UI should provide a login page.<br />
• The airline company has its own fleet of aircraft and a number of flight codes; every code has
a particular source and destination airport, time slot, week day, and the aircraft assigned to it.<br />
• Company employees can view and modify flight codes and company’s fleet, i.e., add/edit/ remove
existing codes and add/remove aircraft. An employee can also issue offers for particular clients
or types of clients (see below).<br />
• Client users or simply clients can register for the system using a sign up page where they provide
personal information, including their email.<br />
• Every time a client flies with the company, she/he earns a predefined number of miles; these
miles are automatically added to her/his account after the flight. The amount of miles depends
on the travelled distance, the type of ticket and the tier of the client (see below).<br />
• Based on the accumulated miles, clients are classified into three tiers; bronze, silver and gold.
Every newly registered client is automatically enrolled to the bronze tier. After earning a particular amount of miles per year the client will be automatically upgraded to silver and from silver
to gold. However, if this miles-requirement is not met in a year the client should be downgraded.<br />
• The above three tiers come with different benefits; e.g., discount on the ticket price, earned miles,
seat upgrade, extra baggage allowance, ticket reservation. You are free to design this benefit
system at will, as long as the differences are clear and the effects can be demonstrated in your
system.<br />
• Through the UI, a logged in client should at least be able to search for flights, buy tickets,
buy luggage and check-in. Also, she/he should be able to check all the information for her/his
account, i.e., current tier, miles earned, flight history and offers. <br />
• The company offers three types of tickets for its flights, economy, business and first class; the
last might not be available on every flight. The type of a ticket, the date of purchase and the
client tier should determine its price and the earned miles.<br />
• After purchasing a ticket, the client should receive an automatic email from the system with
all necessary information; also, two days before the flight another automatic email informs the
client/traveller that the check-in is open.<br />
• A client may ask to cancel a ticket providing a justification. This should appear in the interface
of company’s employees as a pending request in order to accept or reject it.<br />
