if [ -z $1 ]; then
    echo "Please provide a migration name"
    exit 1
fi

beanie new-migration -n $1 -p  ./database/migrations

echo "Migration created successfully"
read -n 1 -s -r -p "Press any key to exit"