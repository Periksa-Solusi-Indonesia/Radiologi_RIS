# PostgreSQL Data Persistence

## Overview

This document explains how PostgreSQL data is persisted in the Radiologi RIS application.

## Changes Made

1. **Docker Compose Configuration Updated**
   - Changed from using a named volume (`postgresql_data`) to a bind mount (`./data/postgresql`)
   - This ensures data is stored directly in the project directory structure

2. **Directory Structure Created**
   - Created `data/postgresql/` directory in the project root
   - Added `.gitkeep` file to ensure directory structure is tracked in git
   - Added `data/README.md` to document the purpose of this directory

3. **Git Configuration Updated**
   - Updated `.gitignore` to ignore the contents of `data/postgresql/` while keeping the directory structure
   - This prevents accidentally committing sensitive database data to version control

## Benefits

1. **Data Persistence**: PostgreSQL data will persist even if containers are removed and recreated
2. **Transparency**: Data is stored in a visible location within the project structure
3. **Backup Simplicity**: The entire data directory can be easily backed up
4. **Version Control**: Directory structure is tracked while actual data is excluded

## Usage

When you start the containers with `docker-compose up`, PostgreSQL will:
1. Create its data files in `./data/postgresql/` if the directory is empty
2. Use existing data files if they already exist
3. Maintain all data across container restarts

## Important Notes

- Never delete the `data/postgresql` directory unless you want to lose all data
- Ensure proper permissions are set if running on Linux systems
- Regular backups of this directory are recommended