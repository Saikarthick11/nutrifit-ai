"""Offline SQLite -> empty PostgreSQL migration; stop the API before running."""
import argparse
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy import create_engine, select
from storage import Store, metadata, conversations, records


def copy_rows(source, target):
    """Copy both tables atomically and verify their full contents before commit."""
    tables=(conversations, records)
    with source.connect() as c:
        data={t.name:[dict(r) for r in c.execute(select(t)).mappings()] for t in tables}
    with target.begin() as c:
        if any(c.execute(select(t).limit(1)).first() for t in tables):
            raise ValueError('Destination is not empty; refusing to overwrite or merge records.')
        for t in tables:
            if data[t.name]: c.execute(t.insert(),data[t.name])
        for t in tables:
            actual={r['id']:dict(r) for r in c.execute(select(t)).mappings()}
            expected={r['id']:r for r in data[t.name]}
            if actual!=expected: raise ValueError('Migration verification failed; transaction rolled back.')
    return {name:len(rows) for name,rows in data.items()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--target-env',type=Path,required=True,help='File containing DATABASE_URL')
    parser.add_argument('--backup-dir',type=Path,required=True)
    args=parser.parse_args()
    if not args.source.is_file(): raise SystemExit('Source SQLite file does not exist.')
    url=dotenv_values(args.target_env).get('DATABASE_URL','')
    if not url.startswith(('postgresql://','postgresql+psycopg://')): raise SystemExit('Target must be PostgreSQL.')
    args.backup_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
    backup=args.backup_dir/('nutrifit-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.db')
    fd=os.open(backup,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    with sqlite3.connect(f'file:{args.source.resolve()}?mode=ro',uri=True) as source,sqlite3.connect(backup) as dest:
        source.backup(dest)
        if dest.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise SystemExit('SQLite integrity check failed.')
    source=create_engine('sqlite:///'+str(backup.resolve()))
    target=Store(url).engine
    try:
        counts=copy_rows(source,target)
    except Exception:
        raise SystemExit('Migration failed; source and backup preserved. Destination must be empty and reachable.') from None
    finally:
        source.dispose();target.dispose()
    print(f'Verified migration: {counts["conversations"]} conversations, {counts["records"]} saved records.')
    print(f'SQLite backup: {backup}')

if __name__=='__main__': main()
