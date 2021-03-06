OMERO.server binary repository
==============================

.. topic:: About

    The OMERO.server binary data repository is a fundamental piece of
    server-side functionality. It provides optimized and indexed storage of
    original file, pixel and thumbnail data, attachments and full-text
    indexes.  The repository's directories contain various files that,
    together with your SQL database, constitute the information about
    your users and their data that OMERO.server relies upon for normal
    operation.

Layout
------

The repository is internally laid out as follows:

::

    /OMERO
    /OMERO/Pixels             <--- Pixel data and pyramids
    /OMERO/Files              <--- Original file data
    /OMERO/Thumbnails         <--- Thumbnail data
    /OMERO/FullText           <--- Lucene full text search index
    /OMERO/ManagedRepository  <--- OMERO.fs filesets, with import logs
    /OMERO/BioFormatsCache    <--- Cached Bio-Formats state for rendering

**Your repository is not:**

-  the "database"
-  the directory where your OMERO.server binaries are
-  the directory where your OMERO.client (OMERO.insight or OMERO.importer)
   binaries are
-  your PostgreSQL data directory

.. _pixelresolutionorder:

PixelService resolution order for locating binary data for images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the server is trying to find the binary data for an image, it looks:

-  first under `/OMERO/Pixels` for a :file:`$NUMBER_pyramid` file
-  then under `/OMERO/Pixels` for a regular :file:`$NUMBER` file
-  then under `/OMERO/Files` for OMERO 4 files
-  or under `/OMERO/ManagedRepository` for OMERO 5 files

Locking and remote shares
-------------------------

The OMERO server requires proper locking semantics on all files in the binary
repository. In practice, this means that remotely mounted shares such as AFS,
CIFS, and NFS can cause issues. If you have experience and/or the time to
manage and monitor the locking implementations of your remote filesystem, then
using them as for your binary repository should be fine.

If, however, you are seeing errors such as NullPointerExceptions, "Bad file
descriptors" and similar in your server log, then you will need to use
directly connected disks.

.. Warning::

    If your binary repository is a remote share and mounting the share fails
    or is dismounted, OMERO will continue operating using the mount point
    instead! To prevent this, make the mount point read-only for the OMERO
    user so that no data can be written to the mount point.

Changing your repository location
---------------------------------

.. note::

    It is **strongly** recommended that you make all changes to your OMERO
    binary repository with the server shut down. Changing the
    :property:`omero.data.dir` configuration does **not** move the repository for
    you, you must do this yourself.

Your repository location can be changed from its :file:`/OMERO` default by
modifying your OMERO.server configuration as follows:

::

    $ cd OMERO.server
    $ bin/omero config set omero.data.dir /mnt/really_big_disk/OMERO

The suggested procedure is to shut down your OMERO.server instance, move
your repository, change your :property:`omero.data.dir` and then start the
instance back up. For example:

::

    $ cd OMERO.server
    $ bin/omero admin stop
    $ mv /OMERO /mnt/really_big_disk
    $ bin/omero config set omero.data.dir /mnt/really_big_disk/OMERO
    $ bin/omero admin start

The :property:`omero.managed.dir` property for the OMERO.fs managed
repository may be adjusted similarly, even to a directory outside
:property:`omero.data.dir`.

.. note::

    The managed repository should be located and configured to allow the
    OMERO server processes fast access to the uploaded filesets that it
    contains.


Access permissions
------------------

Your repository should be owned by the same user that is starting your
OMERO.server instance. This is often either yourself (find this out by
executing ``whoami``) or a separate ``omero`` (or similar) user who is
dedicated to running OMERO.server. For example:

::

    $ whoami
    omero
    $ ls -al /OMERO
    total 24
    drwxr-xr-x   5  omero  omero   128 Dec 12  2006 .
    drwxr-xr-x   7  root    root   160 Nov  5 15:24 ..
    drwxr-xr-x   3  omero  omero  4096 Dec 20 10:13 BioFormatsCache
    drwxr-xr-x   2  omero  omero  1656 Dec 18 14:31 Files
    drwxr-xr-x 150  omero  omero 12288 Dec 20 10:00 ManagedRepository
    drwxr-xr-x  25  omero  omero 23256 Dec 10 19:06 Pixels
    drwxr-xr-x   2  omero  omero    48 Dec  8  2006 Thumbnails


Repository size
---------------

At minimum, the binary repository should be comfortably larger than the
images and other files that users may be uploading to it. It is fine to
set :property:`omero.data.dir` or :property:`omero.managed.dir` to very large
volumes, or to use logical volume management to conveniently increase
space as necessary.
