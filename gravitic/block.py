class Block:
    def __init__(self, specification, pipeline):
        """
        Initialise a production block.
        
        A production block should be a minimal computable unit for 
        part of an analysis.
        """
        self.name = specification['name']
        self.ready = False
        if "inputs" in specification:
            self.input_blocks = [pipeline.blocks[name] for name in specification["inputs"]]
        else:
            self.input_blocks = []
        self.input_data = {}
        for block in self.input_blocks:
            self.input_data.update({filename: data
                                    for filename, data in block.output_files.items()})
        
        if "status" in specification:
            self.status_flag = specification['status']
        else:
            self.status_flag = None

        self.specification_dict = specification
               
    def package(self):
        pass
    
    @property
    def specification(self):
        """
        Return the current Block specification.
        """
        specification = self.specification_dict
        specification['status'] = self.status
        specification['outputs'] = self.output_files
        return specification

    @property
    def status(self):
        return self.status_flag
    
    @status.setter
    def status(self, flag):
        """
        Set the status of this block.
        """
        self.status_flag = flag


class BlockMap:
    def __init__(self):
        self.known_blocks = {}
        # Add the manual block
        self.known_blocks['manual'] = Block
    def register_block(self,name, block):
        self.known_blocks[name] = block
    def __getitem__(self, item):
        return self.known_blocks[item]
blockmap = BlockMap()

