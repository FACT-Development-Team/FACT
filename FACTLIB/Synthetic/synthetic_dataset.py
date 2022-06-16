# Code to generate and add data to the sql database

import os
import sys
import logging
import sqlite3
import concurrent.futures

#from oeis_entry    import parse_oeis_entry
from timer         import start_timer
from exit_scope    import close_when_done
from setup_logging import setup_logging
from sql_synthetic_generator import generate_synthetic_polynomial, 
                                    generate_synthetic_trigonometric, 
                                    generate_synthetic_exponential, 
                                    generate_synthetic_modulo,
                                    generate_synthetic_prime, 
                                    generate_synthetic_periodic,
                                    generate_synthetic_finite,
                                    generate_synthetic_group

dataset_type = 'exponential' # Can be polynomial, trigonometric, exponential, modulo, prime, periodic, finite, group


logger = logging.getLogger(__name__)
def create_database_schema(dbconn):
    """Ensure that the 'oeis_entries' table is present in the database."""

    schema = """
             CREATE TABLE IF NOT EXISTS oeis_entries (
                 oeis_id               INTEGER  PRIMARY KEY NOT NULL, -- OEIS ID number.
                 identification        TEXT,
                 value_list            TEXT     NOT NULL,
                 name                  TEXT     NOT NULL,
                 comments              TEXT,
                 detailed_references   TEXT,
                 links                 TEXT,
                 formulas              TEXT,
                 examples              TEXT,
                 maple_programs        TEXT,
                 mathematica_programs  TEXT,
                 other_programs        TEXT,
                 cross_references      TEXT,
                 keywords              TEXT     NOT NULL,
                 offset_a              INTEGER,
                 offset_b              INTEGER,
                 author                TEXT,
                 extensions_and_errors TEXT
             );
             """

    # Remove superfluous whitespace in SQL statement.
    schema = "\n".join(line[13:] for line in schema.split("\n"))[1:-1]

    # Execute the schema creation statement.

    dbconn.execute(schema)

def process_synthetic_entry(counter):
    import math
    length = int(math.log2(counter//20 + 2))
    print(length)
    entry = None
    if dataset_type == "polynomial":
        entry = generate_synthetic_polynomial(counter, length)
    elif dataset_type == "trigonometric":
        entry = generate_synthetic_trigonometric(counter, length)
    elif dataset_type == "exponential":
        entry = generate_synthetic_exponential(counter, length)
    elif dataset_type == "modulo":
        entry = generate_synthetic_modulo(counter, length)
    elif dataset_type == "prime":
        entry = generate_synthetic_prime(counter, length)
    elif dataset_type == "periodic":
        entry = generate_synthetic_periodic(counter, length)
    elif dataset_type == "finite":
        entry = generate_synthetic_finite(counter, length)
    elif dataset_type == "group":
        entry = generate_synthetic_group(counter, length)
    else:
        raise Exception("Dataset type: " + dataset_type + " is not supported")
    return entry


def process_database_entries(database_filename_in):

    #if not os.path.exists(database_filename_in):
    #    logger.critical("Database file '{}' not found! Unable to continue.".format(database_filename_in))
    #    return

    (root, ext) = os.path.splitext(database_filename_in)

    database_filename_out = database_filename_in #root + "_parsed" + ext

    #if os.path.exists(database_filename_out):
    #    logger.info("Removing stale file '{}' ...".format(database_filename_out))
    #    os.remove(database_filename_out)

    # ========== fetch and process database entries, ordered by oeis_id.

    BATCH_SIZE = 1000 
    print("TEEEEST")
    #g = generate_synthetic_exponential()
    counter = 0
    with start_timer() as timer:
        #with close_when_done(sqlite3.connect(database_filename_in)) as dbconn_in, close_when_done(dbconn_in.cursor()) as dbcursor_in:
        with close_when_done(sqlite3.connect(database_filename_out)) as dbconn_out, close_when_done(dbconn_out.cursor()) as dbcursor_out:

                create_database_schema(dbconn_out)

                with concurrent.futures.ProcessPoolExecutor() as pool:

                    #dbcursor_in.execute("SELECT oeis_id, main_content, bfile_content FROM oeis_entries ORDER BY oeis_id;")

                    while counter < 500000:
                        
                        logger.log(logging.PROGRESS, "Processing OEIS entries B{:06} to B{:06} ...".format(counter, counter + BATCH_SIZE))

                        query = "INSERT INTO oeis_entries(oeis_id, identification, value_list, name, comments, detailed_references, links, formulas, examples, maple_programs, mathematica_programs, other_programs, cross_references, keywords, offset_a, offset_b, author, extensions_and_errors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                        dbcursor_out.executemany(query, pool.map(process_synthetic_entry, [counter + i for i in range(BATCH_SIZE)]))
                        counter += BATCH_SIZE
                        dbconn_out.commit()

        logger.info("Processed all database entries in {}.".format(timer.duration_string()))


def main():

    database_filename_in = "oeis_parsed.sqlite3"

    (root, ext) = os.path.splitext(database_filename_in)
    logfile = root + ".log"

    with setup_logging(logfile):
        process_database_entries(database_filename_in)


if __name__ == "__main__":
    main()
