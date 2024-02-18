clear &&

# Create the needed directories
# if they don't exist
if [ ! -d obj ]; then
	echo "Directory ./obj doesn't exist, creating"
	mkdir obj
fi

if [ ! -d bin ]; then
	echo "Directory ./bin doesn't exist, creating"
	mkdir bin
fi

# Clean them just in case
rm -rf ./obj/* &&
rm -rf ./bin/* &&

# Compile
make &&
# Transfer to calculator
tilp --no-gui ./bin/*.8xp*