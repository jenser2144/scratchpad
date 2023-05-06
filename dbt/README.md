# dbt Test Project
## Deployment
### Secret Variables
Create `.env` file in root folder with the following variables:
- `HOST=database host name`
- `USER=user name for database`
- `PASS=password for database`

### Build/Destroy
- Build: `make up`
- Destroy: `make down`

## Source Code
Source code is stored in the `src` folder
- `src/test_dbt_project` is the initialized dbt folder

## Configuration Files
- `.gitignore`
- `docker-compose.yml` - containerized orchestration of dbt
- `Makefile` - Build/Destroy executor
- `build.sh` - bash commands for build
- `requirements.txt` - use to list python src modules required for a repo