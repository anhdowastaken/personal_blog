TOKEN=""

while [[ $# -gt 0 ]]
do
  key="$1"

  case $key in
    -t|--token)
      TOKEN=$2
      shift # past argument
      ;;
    -h|--help)
      echo "usage:"
      echo "-t|--token <Dropbox token string>"
      exit 0
      ;;
    *)
      # unknown option
      ;;
  esac
  shift # past argument or value
done

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# Go to backend directory
cd $DIR
# Active virtual environment
source venv/bin/activate
# Generate and upload backup
python3 backup_db.py -t $TOKEN
