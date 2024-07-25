import shortuuid
import uuid
import time


def get_sft_txt(data_js, dtype='s1'):
    """
    函数作用：根据SFT数据，拼接其问答的文本信息。（将来可用于生成sft_id）。
        data_js：SFT数据
        dtype: SFT数据格式，s1或s2
    返回结果：SFT数据中问答拼接字符串。
    """
    qa_list = []
    if dtype == 's1':
        # history
        if data_js.get('history') is not None:
            his = data_js['history']
            if not isinstance(his, list):
                his = eval(his)
            for itr in his:
                for sub_itr in itr:
                    qa_list.append(str(sub_itr).strip())
        # instruction -> input -> output
        for itr in ['instruction', 'input', 'output']:
            if data_js.get(itr) is not None:
                qa_list.append(str(data_js[itr]).strip())
        # 返回sft-txt拼接结果
        qa_txt = '\n'.join([itr for itr in qa_list if itr != ''])
        if qa_txt == '':
            print('请确认输入的SFT数据是s1格式，当前数据没有获取到 instruction, input, output, history 任何一个字段！')
    if dtype == 's2':
        if data_js.get('conversations') is None:
            print('请确认输入的SFT数据是s2格式，当前数据没有 conversations 字段！')
        else:
            for itr in data_js['conversations']:
                value_ = itr.get('value', '')
                qa_list.append(str(value_).strip())
        # 返回sft-txt拼接结果
        qa_txt = '\n'.join([itr for itr in qa_list if itr != ''])
    return qa_txt


# =================== (1) 生成22位uuid ===================
def get_id_22d(txt):
    """
    根据指定的文本txt生成uuid,一般txt文件路径+文件名
    """
    uid5 = uuid.uuid5(uuid.NAMESPACE_DNS, txt)  # 32位
    uid_short = shortuuid.encode(uid5)  # 32位为转22位
    return uid_short


# =================== (2) 生成10位uuid ===================
"""基于Python生成短10位唯一id"""


def get_id_10d(base_str):
    array_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  # "A", "B", "C", "D", "E", "F", "G", "H", "I","J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V","W", "X", "Y", "Z"
                  ]
    array_len = len(array_list)

    id_ = str(uuid.uuid5(uuid.NAMESPACE_DNS, base_str)).replace("-", '')  # 32位

    # 存储从id_z中截取的子串
    sub_num = []
    # 1. id_分为为 8个4位子串
    for i in range(0, 8):
        start = i * 4
        zz_num = id_[start: start + 4]
        sub_num.append(zz_num)
    # 2. 尾头片接子串
    add1 = id_[-2:] + id_[:2]
    sub_num.append(add1)
    # 3. 中间子串
    add2 = id_[14:18]
    sub_num.append(add2)

    # 计算对应的index
    index_ = [int(val, 16) % array_len for val in sub_num]
    # index对应的字符
    id_list = [array_list[i] for i in index_]

    return ''.join(id_list)


# =================== (3) 生成雪花id ===================
class Snow:
    """雪花算法生成全局自增唯一id"""
    init_date = time.strptime('2020-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
    start = int(time.mktime(init_date) * 1000)
    last = int(time.time() * 1000)
    pc_room = 1
    pc = 1
    seq = 0

    @classmethod
    def get_guid(self):
        """获取雪花算法生成的id"""
        now = int(time.time() * 1000)
        if now != self.last:
            self.last = now
            self.seq = 1
        else:
            while self.seq >= 4096:
                time.sleep(0.1)
                return self.get_guid()
            self.seq += 1

        time_diff = now - self.start
        pk = (time_diff << 22) ^ (self.pc_room << 18) ^ (self.pc << 12) ^ self.seq

        return pk


def gen_snowid():
    snow_id = Snow()
    return snow_id.get_guid()


"""基于Python生成短12位唯一id"""


def get_self_id(base_str):
    array_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z"
                  ]
    array_len = len(array_list)

    special_symbol = ["!", "@", "#", "$", "%", "^", "&", "*", "/", "-", "_", "=", "+"]
    special_len = len(special_symbol)

    id_ = str(uuid.uuid5(uuid.NAMESPACE_DNS, base_str)).replace("-", '')  # 32位

    # 存储从id_z中截取的子串
    sub_num = []
    # 1. id_分为为 8个4位子串
    for i in range(0, 8):
        start = i * 4
        zz_num = id_[start: start + 4]
        sub_num.append(zz_num)
    # 2. 尾头片接子串
    add1 = id_[-2:] + id_[:2]
    sub_num.append(add1)
    # 3. 中间子串
    add2 = id_[14:18]
    sub_num.append(add2)

    add2 = id_[2:6]
    sub_num.append(add2)

    add2 = id_[-6:-2]
    sub_num.append(add2)

    # 计算对应的index
    id_list = []
    for i, val in enumerate(sub_num):
        if i in [3, 11]:
            index_ = int(val, 16) % special_len
            id_list.append(special_symbol[index_])
        else:
            index_ = int(val, 16) % array_len
            id_list.append(array_list[index_])

    return ''.join(id_list)
