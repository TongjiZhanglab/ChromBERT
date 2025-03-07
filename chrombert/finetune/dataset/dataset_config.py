import os 
import json
import numpy as np
from typing import Optional, Union, IO, Any, Dict
from copy import deepcopy

class DatasetConfig:
    
    def __init__(self, config: Union[str, Dict[str, Any], "DatasetConfig"] = None, **kwargs: Any):
        '''
        DatasetConfig is a class that defines the configuration of the dataset.
        Args: 
        [general]
            hdf5_file: str or IO, the path to the reference cistromes, downloaded from the link we provided.
            supervised_file: str or IO, the path to samples for forward.
            kind: str, the class name of the dataset, one of ["BasicDataset","GeneralDataset","PerturbationDataset","MultiFlankwindowDataset","PromptDataset"]
            meta_file: str, path of a json file (downloaded from our website) that contains the preset prompt information. Can be ignored if no ignore or prompt is set.

        [ignore]
            ignore: bool, whether to ignore some regulators or gsmids.
            ignore_object: str or list, the regulators to be ignored.

        [dataloader]
            batch_size: int, the batch size of the dataloader.
            num_workers: int, the number of workers of the dataloader.

        [perturbation]
            perturbation: bool, whether to perturb the input. If True, the input will be perturbation.
            perturbation_object: str, perturbation object, example: 'ep300,crebbp' or 'ep400' or 'GSM1036403,GSM1070124,GSM1022944'. 
            perturbation_value: int, the value to be perturbation. 0 for knock-out and 1 for overexpression. 

        [prompt]
            prompt_kind: str, the class name of the prompt, one of ["expression", "cistrome", "dna"]

            [prompt.expression or prompt.cistrome]
                prompt_regulator_cache_file: str, the path to the regulator prompt cache file. for accelerating large scale prediction. See tutorial for more details. 
                prompt_celltype_cache_file: str, the path to the celltype prompt cache  file, for accelerating large scale prediction. See tutorial for more details. 

                prompt_regulator: str, the regulator prompt. Determine the kind of output. For example, "ctcf" or "h3k27ac". It can also be provided in the supervised file if the format supports. Ignored for "dna". 
                prompt_celltype: str, the celltype of the expression/cistrom prompt. (e.g. k562 for expression prompt, atac:k562 for cistrom prompt). It can also be provided in the supervised file if the format supports.

            [prompt.dna]
                fasta_file: str, the path to the fasta file.


        [multi window]
            flank_window: int, the flank window size.
        '''
        
        # [general]
        self.hdf5_file: Union[str, IO] = None
        self.supervised_file: Union[str, IO, None] = None
        self.kind: str = None
        self.meta_file: str = None

        # [ignore]
        self.ignore: bool = False
        self.ignore_object: str = None
        

        # [dataloader]
        self.batch_size: int = 8
        self.num_workers: int = 20
        self.shuffle: bool = False
        self.pin_memory: bool = True

        # [perturbation]
        self.perturbation: bool = False
        self.perturbation_object:str = None
        self.perturbation_value: Optional[int] = 0

        # [prompt]
        self.prompt_kind: str = None
        self.prompt_regulator: str = None
        self.prompt_regulator_cache_file: str = None
        self.prompt_celltype: str = None
        self.prompt_celltype_cache_file: str = None

        self.prompt_regulator_cache_pin_memory: bool = False
        self.prompt_regulator_cache_limit: int = 3
        
        # [prompt.dna]
        self.fasta_file: str = None
        
        # [multi window]
        self.flank_window: int = 0

        if config is not None:
            self.load(config)
        self.update(**kwargs)
        self.validate()
            
    @property
    def vocab_shift(self):
        return 5 
    
    @property
    def vocab_levels(self):
        return 5

    @property
    def token_id_pad(self):
        return 0

    @property
    def position_id_pad(self):
        return 0

    def validate(self):
        kinds = ["BasicDataset","GeneralDataset","MultiFlankwindowDataset","PromptDataset"]
        if self.kind not in kinds:
            raise ValueError(f"kind must be one of {kinds}, but got {self.kind}!")

        if self.perturbation and self.perturbation_value is None:
            raise AttributeError("perturbation_value should be set when perturbation is set True!")
        return None

    def load(self, config):
        if isinstance(config, type(self)):
            for key, value in config.to_dict().items():
                setattr(self, key, value)
            return None 
        
        valid_fields = set(self.__dict__.keys())
        if isinstance(config, str):  
            with open(config, 'r') as f:
                config = json.load(f)
        if isinstance(config, dict):  
            for key, value in config.items():
                if key in valid_fields:
                    setattr(self, key, value)
                else:
                    raise AttributeError(f"Warning: '{key}' is not a valid field name in DatasetConfig")
        return None       

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Warning: '{key}' is not a valid field name in DatasetConfig")
        return None 

    def save(self, config_file: str):
        values = self.to_dict()
        with open(config_file, 'w') as f:
            json.dump(values, f, indent=4)
        return None 

    def __repr__(self):
        values = self.to_dict()
        return f"DatasetConfig({values})"
    
    def __str__(self):
        values = self.to_dict()
        return json.dumps(values, indent=4)
    
    def to_dict(self):
        return {key: deepcopy(getattr(self, key)) for key in self.__dict__.keys()}
        
    def items(self):
        return self.to_dict().items()
    
    def clone(self, **kwargs):
        dc =  DatasetConfig(config=self.to_dict())
        dc.update(**kwargs)
        return dc
    
    def init_dataset(self, return_config = False, **kwargs):
        '''
        A method to instantiate the dataset object. Args are the same as DatasetConfig. 
        '''
        new_config = self.clone()
        new_config.update(**kwargs)
        if self.kind == 'GeneralDataset':
            from .general_dataset import GeneralDataset
            ds = GeneralDataset(config=new_config)
        elif self.kind == 'MultiFlankwindowDataset':
            from .multi_flankwindow_dataset import MultiFlankwindowDataset
            ds =  MultiFlankwindowDataset(config=new_config)
        elif self.kind == 'PromptDataset':
            from .prompt_dataset import PromptDataset
            ds =  PromptDataset(config=new_config)
        else:
            raise AttributeError(f"Warning: '{self.kind}' is not a valid dataset class")
        if return_config:
            return ds, new_config
        return ds
        
    def init_dataloader(self, **kwargs):
        dataset, dc = self.init_dataset(return_config= True, **kwargs)
        from torch.utils.data import DataLoader
        
        dataloader = DataLoader(
            dataset,
            batch_size=dc.batch_size,
            shuffle=dc.shuffle,
            num_workers=dc.num_workers
        )
        return dataloader

def get_preset_dataset_config(preset: str = "default", basedir: str = os.path.expanduser("~/.cache/chrombert/data"),**kwargs):
    '''
    A method to get the preset dataset configuration.
    Args:
        preset: str, the pre-defined preset name of the dataset, or defined by user self.
        basedir: str, the basedir of the preset file. Default is "~/.cache/chrombert/data".
        kwargs: dict, the additional arguments to update the preset. See chrombert.DatasetConfig for more details.
    '''
    assert "supervised_file" in kwargs, "supervised_file must be provided"
    basedir = os.path.abspath(basedir)
    assert os.path.exists(basedir), f"{basedir=} does not exist"
    if not os.path.exists(preset):
        list_presets_available = os.listdir(os.path.join(os.path.dirname(__file__), "presets"))
        list_presets_available = [x.split(".")[0] for x in list_presets_available]

        if preset not in list_presets_available:
            raise ValueError(f"preset must be one of {list_presets_available}, but got {preset}")

        preset_file = os.path.join(os.path.dirname(__file__), "presets", f"{preset}.json")
    else:
        preset_file = preset
    with open(preset_file, 'r') as f:
        config = json.load(f)
    config.update(kwargs)
    for key, value in config.items():
        if key.endswith("_file") and key != "supervised_file":
            # print(key, value)
            print(f"update path: {key} = {value}")
            if value is not None:
                if os.path.abspath(value) != value:
                    config[key] = os.path.join(basedir, value)
                    assert os.path.exists(config[key]), f"{key}={config[key]} does not exist"

    dc = DatasetConfig(**config)
    return dc
    
