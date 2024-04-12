# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
#
# # 定义语料库
# corpus = [
#     "I love to eat apples.",
#     "Apples are delicious.",
#     "I enjoy eating apples and oranges."
# ]
#
# # 创建CountVectorizer对象，用于计算词频
# vectorizer = CountVectorizer()
#
# # 对语料库进行词频统计
# word_counts = vectorizer.fit_transform(corpus)     #存储为稀疏矩阵，需要转换为 array 才能查看
# print(word_counts.toarray())
#
# # 创建TfidfTransformer对象，用于计算TF-IDF
# tfidf_transformer = TfidfTransformer()
#
# # 对词频矩阵进行TF-IDF转换
# tfidf_matrix = tfidf_transformer.fit_transform(word_counts)
# print(tfidf_matrix.toarray())
#
# # 获取特征词列表
# feature_names = vectorizer.get_feature_names()
# print(feature_names)
#
# # 打印每个句子的TF-IDF向量
# for i in range(len(corpus)):
#     sentence = corpus[i]
#     tfidf_vector = tfidf_matrix[i]
#     print("Sentence:", sentence)
#     print(tfidf_vector.toarray())
#     for j in range(len(feature_names)):
#         feature_name = feature_names[j]
#         tfidf_value = tfidf_vector[j]
#         print(feature_name)
#         print(tfidf_value.toarray())
#         if tfidf_value > 0:
#             print("  Word:", feature_name, "  TF-IDF:", tfidf_value)
# exit()

import re
import copy
import unicodedata
# text = "I love- to- eat- and apples-oranges ."
# word = "and apples-oranges"
#
# pattern3 = rf'((?:\b\w+-[\s]*){{0,3}})\b{re.escape(word)}\b'
# matches = re.findall(pattern3, text)
# string = str(matches[0])
# tag = word.split('-')
# print(tag)
# for org_word in string.split():
#     text = text.replace(org_word, org_word+tag[1])
# print(matches)
# print(text)

para = 'Polymorphs γ-SUM and α-SUM, like a pair of β-SUM and α-SUM, due to the difference in СР6, are topological (or reconstructive) isomers. At the same time, topologically and chemically identical 3D frameworks β- and γ-SUM with the same СР6 should be considered as different “deformation” forms, since the structural units forming the framework differ in point symmetry due to small mutually consistent displacements of atoms. Thus, in β-SUM, uranyl ions, succinate ions, and water molecules have local C1 symmetry, while in γ-SUM they all have C2 symmetry. As a result, the uranyl succinate 3D framework in β-SUM has monoclinic symmetry and is characterized by the space group P21/n, while the analogous framework in γ-SUM has a higher orthorhombic symmetry, which is described by the space group Pnna.'
#para ='where Ωi is the solid angle (as a percentage of 4π sr) at which the common VDP face of the U and Oi atoms is “visible” from the nucleus of any of them. For example, for the oxygen atoms of the UO22+ groups in I–III, the solid angle averages 21.6(2)%. Therefore, the value of Ei for the oxygen atom of the uranyl ion (O2–//M1: hereinafter, the symbol of the ligand coordination type with respect to the uranium atom is indicated after the double slash), calculated by Eq. , is 3.89(4) ≈ 4ē. This result is in good agreement with the classical view of the structure of the UO22+ group, according to which each U=O bond in the uranyl ion is created by two shared electron pairs, i.e., 4 electrons. Note also that the indicated Ei calculated on the basis of data for I–III practically coincided with Ei(О2–//M1) = 3.9(1)ē for more than 300 U=O bonds in the structures of sulfate, nitrate, or carbonate-containing uranyl complexes [–]. According to R-18, the U(VI) atom gains the missing (18.0 – 2×3.9) = 10.2ē due to the formation of equatorial U–O bonds, which according to classical concepts are single, since each of them corresponds to about 2 electrons.'
#para ='As noted [–], according to R-18, the realized coordination number of U(VI) atoms depends on the electron-donating ability of oxygen atoms that comprise the UOn CP. For the convenience of calculations, it is assumed that the U(VI) atom in the UOn CP is the U6+ ion, which is an acceptor of electrons donated by coordinated oxygen atoms. All oxygen atoms in the UOn CP are electron donors, and the number of electrons (Ei) donated to the U6+ ion by one Оi atom of some ligand can be determined from the relation'
#para = 'As it is known, U(VI) atoms chemically bonded only to oxygen atoms most often form the UOn CP at n = 6, 7, or 8 [–]. It has been repeatedly noted that the VDP volume of U(VI) atoms in UOn complexes is practically independent of the uranium CN and is, on average, 9.2(2) Å3 []. The constancy of the VDP volume is considered as a consequence of a stable and uniform electron shell (presumably 18ē) afforded by the U(VI) atoms. Based on this hypothesis, the 18-electron rule (hereinafter R-18), which allows predicting the possible coordination number of U(VI) atoms in uranyl complexes, is successfully used in the analysis of a number of water-salt systems, in particular, containing sulfate- [], nitrate- [], carbonate- [], methacrylate- [], or propionate-ions [], as well as in the case of revealing structural features of stoichiometrically similar complexes [UO2XO4]z–, where Х = Si(IV), P(V) or S(VI) [].'
#para = 'The difference in the structure of uranyl succinate frameworks can be characterized by coordination sequences {СРN} [], indicating the number (СР) of metal A atoms, which are bound to the base by all bridging ligands of the first (N = 1), second (N = 2), and subsequent coordination spheres. According to the data obtained, for the first six coordination spheres in the α-modification {СР6 = 12, 60, 152, 274, 442, 632}, and for β- or γ-SUM {СР6 = 10, 42, 92, 162, 252, 362}. As already noted [], due to different {СРN}, α- and β-SUM are topological isomers, and the difference in the structure of their 3D frameworks is a consequence of different conformation  of succinate ions. In this regard, it can be noted that the C–C–C–C torsion angles (φ) for succinate ions in the α-, β-, and γ-SUM structures are 180.0°, 67.2°, and 67.0°, respectively. Since the φ angles for β- and γ-SUM practically coincide, it is not surprising that the СР6 parameters for these polymorphs do not differ.'
#para = 'All SUM polymorphs contain one independent U atom, which occupies a position with the C2, Cs, or C1 symmetry and forms the UO7 CP. As in the α- or β-forms, the UO7 CP in γ-SUM (II) is a pentagonal bipyramid, in which four equatorial oxygen atoms belong to four different succinate ions, and the fifth atom is part of the water molecule, which, like the uranium atom, lies on the C2 axis. Water molecules play the role of monodentate ligands, while succinate ions exhibit the Q4 coordination type . The same crystallochemical role of succinate ions and water molecules is also demonstrated in the α- or β-SUM structures. Therefore, the structures α-, β-, and γ-SUM correspond to a single crystal chemical formula АQ4M1, where A = UO22+, Q4 = C4H4O42–, and M1 = H2O. Due to the bridging succinate ions Q4 (each of them binds the basic U atom with three others), all three polymorphs have a 3D structure.'
#para = 'Succinate-containing U(VI) compounds belong to the class of organo-uranium coordination polymers, which have been fairly actively studied in recent decades [–]. Lately, it was found that succinate ions (C4H4O42– = suc2–), which belong to the homologous series of [O2C–(CH2)n–CO2]2– dianions of aliphatic dicarboxylic acids, can exhibit 10 topologically different types of coordination to f-metal atoms []. The available data indicate that even with the same suc2– : UO22+ ratio, the polymers resulting due to topological isomerism can differ in dimension (1D, 2D, or 3D) and in the structure of the formed uranyl succinate complexes. It was also found that in some UO2(suc)–L–H2O systems, where L is an electrically neutral nitrogen-containing ligand , in the structure of the resulting crystals of the composition UO2(suc)·nL (excluding crystallization water molecules), two types of U(VI) complexes coexist, which can be considered as products of disproportionation according to the scheme 3UO2(suc)·nL → [UO2(L)х]2+ + [(UO2)2(suc)3]2– + (3n – x)L.'

def para_clean(paragraph):
    pattern = r'\b(and|or)\s+(\w+-\w+)'
    pattern4 = r','
    str = re.findall(pattern, paragraph)  # 最好不能重复
    matches = re.finditer(pattern, paragraph)
    # print(str)
    # print(list(matches))
    if re.findall(pattern, paragraph):
        para = copy.copy(paragraph)
        para= re.sub(pattern4, '', para)
        head = 0
        text = ''
        for words in re.finditer(pattern, paragraph):        #注意para和paragraph的区别
            word = words.group()
            print(word)
            tail = words.end()
            tag_words = words.group(2).split('-')
            pattern3 = rf'((?:\b\w+-[\s]*){{0,5}})\b{re.escape(word)}\b'
            if not re.findall(pattern3, para)[0]:           #是一个包含空字符串的列表而不是一个空列表，匹配式中使用了零宽度匹配，例如*
                txt = paragraph[head:tail]
                print(txt)
            #     print('true')
            #     return paragraph
            string = re.findall(pattern3, para)[0]
            print(re.findall(pattern3, para))
            for i in range(len(string.split())):
                if i < 1:
                    txt = paragraph[head:tail].replace(string.split()[i], string.split()[i] + tag_words[1])
                else:
                    txt = txt.replace(string.split()[i], string.split()[i] + tag_words[1], 1)
                print(txt)
            text += txt
            print('>>>>>>>>><<<<<<<<<')
            head = tail

        text += paragraph[tail:]
        print(text)
        print(paragraph)
        return text
    else:
        return paragraph
if __name__ == '__main__':
    pattern = r'\[[^\w\d]*?\]'
    pattern1 = r'\[[\-\d\,\ ]*?\]'
    pattern2 = r'\b(and|or)\s+(\w+-\w+)'
    para = re.sub(pattern1, '',re.sub(pattern, '', unicodedata.normalize('NFKC', para.replace("\n", " ").replace("\t", ""))))
    print(para)
    text = para_clean(para)
    #print(text)
    exit()

import regex as re
from nltk.corpus import wordnet
word = 'cm–1'
split_words = word.split('-')
# print(split_words)
# print([len(wordnet.synsets(word)) for word in split_words if wordnet.synsets(word)])
# if len(split_words) == len([len(wordnet.synsets(word)) for word in split_words if wordnet.synsets(word)]):
#     print('拆分成两个单词')
#     print(' '.join(split_words))
# else:
#     print('不可以拆分成两个单词')
for word in split_words:
    print(word)
    if word.lower() in wordnet.words():       #词典判别需要将单词小写，同义词集不用
        print('true')
        print(1)
    if wordnet.synsets(word):
        print('true')
        print(2)

exit()
s = '=carbonate- , methacrylate- , or propionate-ions α-, β-, and γ-SUM structures like apples- and'
pattern = r'\b(and|or)\s+(\w+-\w+)'       #
pattern1 = r'(\b[\p{L}\p{P}]+-\s,) β- ,'      #匹配字母，标点符号和拉丁数字
pattern2 = r'[\p{L}\p{P}|-]\,'
pattern4 = r','
pattern5 = r'\b\w+-\w+\b'
print(re.findall(pattern5,s))
s = re.sub(pattern2,'- ,', s)
print(s)
match = re.findall(pattern1,s)
print(match)
str = re.findall(pattern, s)     #最好不能重复
print(str)
for words in str:
    print(words)
    print(words[0] + ' ' + words[1])
    split_words = words[1].split('-')
    print(split_words)
    print([wordnet.synsets(word) for word in split_words if len(wordnet.synsets(word))>0])
    if all([wordnet.synsets(word) for word in words if len(wordnet.synsets(word))>0]):
        print(1)
        s = s.replace(words[1], ' '.join(split_words))
exit()
print(re.findall(pattern, para))
paragraph = copy.copy(para)
paragraph = re.sub(pattern4,'', paragraph)
print(paragraph)
if re.findall(pattern, paragraph):
    head = 0
    text = ''
    for words in re.findall(pattern, paragraph):
        word = words[0] + ' ' + words[1]
        print(word)
        tail = para.find(word) + len(word)
        tag_words = words[1].split('-')
        pattern3 = rf'((?:\b\w+-[\s]*){{0,3}})\b{re.escape(word)}\b'
        string = re.findall(pattern3, paragraph)[0]
        # print(string)
        # print(string.split())
        # print(re.findall(pattern3, paragraph))
        for i in range(len(string.split())):
            # print((string.split()[i]))
            # print(tag_words[1])
            # print(para[head:tail])
            if i < 1:
                txt = para[head:tail].replace(string.split()[i], string.split()[i] + tag_words[1])
            else:
                txt = txt.replace(string.split()[i], string.split()[i] + tag_words[1],1)
            print(txt)
        text += txt
        #print(text)
        print('>>>>>>>>><<<<<<<<<')
        head = tail

    text += para[tail:]
    print(text)
    print(para)
else:
    print('>>>>>>>>>无特殊句式或可处理的特殊单词<<<<<<<<<,')
exit()


from nltk.corpus import wordnet

def is_word(word):
    synsets = wordnet.synsets(word)
    return len(synsets) > 0

# 示例用法
word1 = 'ions'

print(is_word(word1))  # 输出: True

exit()



#给披肩自动编码器来个数据降维
# from keras.layers import Input,Dense,Concatenate
# from keras.models import Model
# #堆叠式自动编码器
# input_topics = Input(shape = (topic.shape[1],))
# input_embeddings = Input(shape = (embedding.shape[1],))
#
# #520w维降到16维度
# encoded = Dense(16,activate = 'relu')(x)
#
# autoencoder = Model([input_topics,input_embeddings],x)
# encoded_output = encoder.predict([topics,embeddings])


import regex as re
s = 'with the metastable α-(NH4)LiSO4 (ref. ) (Fig. . Likewise  are shown in Fig.  .'
s1='with the metastable α-(NH4LiSO4  ( . Likewise  are shown in  .'
pattern1 = r'\(ref. \)'
pattern2 = r'\bFig.\s'
pattern3 = r'\s[\(\)]\s'
str = re.sub(pattern1, '', s)
str1 = re.sub(pattern2, '', s)
print(re.sub(pattern3, '',re.sub(pattern2, ' ',re.sub(pattern1, '',s))))
print(re.search(pattern3,s1))
exit()
#去除所有半角全角符号，只留字母、数字、中文。

# 去除所有半角全角符号，只留字母、数字、中文。
def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line
# python3直接用下面的:
    re.findall('[a-zA-Z0-9\u4e00-\u9fa5]', string)

# 只留中文。
# python3直接用下面的:
    re.findall('[a-zA-Z0-9\u4e00-\u9fa5]', string)

#在前面加”ur“，u的意思是表明后面有Unicode字符，汉字的范围为”\u4e00-\u9fa5“，这个是用Unicode表示的，所以前面必须要加”u“；字符”r“的意思是表示忽略后面的转义字符，这样简化了后面正则表达式里每遇到一个转义字符还得挨个转义的麻烦
s = 'you get:"Python\xa0"'
print(s.replace('\xa0', ' '))

# 括号表达式 Match matchData = Regex.Match(characterString, "(\\[).*?(\\])"
