Gravitic
========

Gravitic is a tool which is designed to make designing analysis and training pipelines easy.

It was developed to make creating new pipelines for analysing gravitational wave data, removing the need to create new infrastructure for data handling.
Gravitic builds pipelines from blocks, allowing individual parts to be swapped easily, and simplifying the process of prototyping new analyses.

Asimov
------

Gravitic is designed from the ground-up to be compatible with LIGO's asimov toolkit, allowing gravitic pipelines to be managed and automated using the same tools used for established pipelines.

Documentation
-------------

Do I need gravitic?
-------------------

We designed Gravitic to make it easier to prototype new machine learning components in analyses, while not needing to put together infrastructure for tasks such as trigger detection, data handling, and results post-processing.

If you're working on some small part of a larger analysis, like a new sampler, new waveform model, or event a new trigger generator, then gravitic can make your life easier.

Installing gravitic
-------------------

Gravitic is written in Python.
At the moment you'll still need to install it from source by running ::

  $ pip install .

in the root of the project repository.

Get started
-----------

Roadmap
-------

Contributing
------------

Authors
-------

Gravitic is made by Daniel Williams, and its development is supported by the University of Glasgow and the Science and Technology Facilities Council.

License
-------
