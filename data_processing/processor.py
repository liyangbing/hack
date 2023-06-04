class Processor:
    """一个用于处理数据的基础类"""

    def load_data(self):
        """从源加载数据，需要在子类中具体实现"""
        raise NotImplementedError

    def split_data(self):
        """将输入数据进行分割，需要在子类中具体实现"""
        raise NotImplementedError

    def display_info(self, data):
        """显示数据的基本信息"""
        print(f'There are {len(data)} documents in your data.')
        print(f'The first document contains {len(data[0].page_content)} characters.')
