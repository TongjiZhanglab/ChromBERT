chrombert_imputation_cistrome_sc
************************************

Generate prediction result (hdf5 format) from ChromBERT when given single cell, region and regulator.

.. code-block:: shell

    chrombert_imputation_cistrome_sc [OPTIONS] SUPERVISED_FILE --o-h5 H5_PATH --finetune-ckpt CKPT --prompt-kind KIND

.. rubric:: Options

.. option:: supervised_file

    Path to the supervised file.

.. option:: --o-h5

    Path of the output HDF5 file. This option is required.

.. option:: --prompt-kind

Prompt data class. Choose from *cistrome* or *expression*. This option is required.

.. option:: --basedir

    Base directory for the required files. Default is set to the value of `DEFAULT_BASEDIR`.

.. option:: -g, --genome

    Genome version. For example, *hg38* or *mm10*. Only *hg38* is supported now. Default is *hg38*.

.. option:: --pretrain-ckpt

    Path to the pretrain checkpoint. Optional if it could be inferred from other arguments.

.. option:: -d, --hdf5-file

    Path to the HDF5 file that contains the dataset. Optional if it could be inferred from other arguments.

.. option:: -hr, --high-resolution

    Use 200-bp resolution instead of 1-kb resolution. Caution: 200-bp resolution is preparing for the future release of ChromBERT, which is not available yet.

.. option:: --finetune-ckpt

    Path to the finetune checkpoint. Optional.

.. option:: --prompt-dim-external

    Dimension of external data. Use *512* for *scGPT* and *768* for *ChromBERT*'s embedding. Default is *512*.

.. option:: --prompt-celltype-cache-file

    Path to the cell-type-specific prompt cache file. Optional.

.. option:: --prompt-regulator-cache-file

    Path to the regulator prompt cache file. Optional.

.. option:: --prompt-regulator-cache-pin-memory
    Pin memory for regulator prompt cache for further accelerating. Default is False. 

.. option:: --prompt-regulator-cache-limit
    The limit of regulator prompt cached in memory. Be mindful of your memory usage! 

.. option:: --prompt-celltype

    The cell-type-specific prompt. For example, *dnase:k562* for cistrome prompt and *k562* for expression prompt. It can also be provided in the supervised file if the format supports. Optional.

.. option:: --prompt-regulator

    The regulator prompt. Determine the kind of output. For example, *ctcf* or *h3k27ac*. It can also be provided in the supervised file if the format supports. Optional.

.. option:: --batch-size

    Batch size. Default is *8*.

.. option:: --num-workers

    Number of workers for the dataloader. Default is *8*.
