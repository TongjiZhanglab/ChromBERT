Compiled Scripts for fine-tuning of ChromBERT
=============================================


Overview
----------

For a hands-on tutorial, see the documentation on :doc:`tutorial_finetuning_ChromBERT_from_scratch`.  

We provide three scripts for fine-tuning, designed for your convenience. All scripts can be downloaded and executed anywhere, provided that your installation is correct.

For detailed usage instructions, run the following command:

.. code-block:: bash

    python <script.py> --help

.. csv-table:: Fine-Tune Scripts
    :header: "Type", "Download", "Description"

    "`General`_", "`download <https://raw.githubusercontent.com/TongjiZhanglab/ChromBERT/main/examples/train/ft_general.py>`_ ", "Suitable for most purposes."
    "`Prompt-enhanced`_", "`download <https://raw.githubusercontent.com/TongjiZhanglab/ChromBERT/main/examples/train/ft_prompt_enhanced.py>`_", "Designed for prompt-enhanced tasks, such as cistrome generation."
    "`Gep`_", "`download <https://raw.githubusercontent.com/TongjiZhanglab/ChromBERT/main/examples/train/ft_gep.py>`_", "Intended for tasks that use multiple 1-kb bins as input, such as gene expression prediction."

Details 
---------

.. include:: scripts/ft_general.rst

----

.. include:: scripts/ft_prompt_enhanced.rst

----

.. include:: scripts/ft_gep.rst