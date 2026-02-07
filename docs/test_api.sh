"""
Django API Tests using curl
"""

# Test Destinations
echo "=== Get All Destinations ==="
curl -X GET http://localhost:8000/api/destinations/

echo "\n=== Search Destination ==="
curl -X GET "http://localhost:8000/api/destinations/search/?name=Agra"

# Test Hotels
echo "\n=== Get All Hotels ==="
curl -X GET http://localhost:8000/api/hotels/

echo "\n=== Search Hotels ==="
curl -X GET "http://localhost:8000/api/hotels/search/?location=Agra"

# Test Cabs
echo "\n=== Get All Cabs ==="
curl -X GET http://localhost:8000/api/cabs/

echo "\n=== Filter Cabs ==="
curl -X GET "http://localhost:8000/api/cabs/filter/?vehicleType=economy"

# Test Contacts
echo "\n=== Submit Contact ==="
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210",
    "subject": "Test Message",
    "message": "This is a test message"
  }'

echo "\n=== Get All Contacts ==="
curl -X GET http://localhost:8000/api/contacts/
