import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, nargs='?',default='', help="pickle file with clusters dataframe")
#parser.add_argument("outfolder", type=str, nargs='?',default='', help="output folder")
args = parser.parse_args()
file = args.file
#outfolder = args.outfolder

imdict = {'2474_3':"https://drive.google.com/uc?id=1jIbh9iCI_7_PriSju99Y_MjheUjwocMH",
          '2474_6':"https://drive.google.com/uc?id=11rZANHn19r9ZNeSDkTy32nqzA0FCPjXa",
          '2483_11':"https://drive.google.com/uc?id=1CiwkadaRE4U-ccDfw9urJJi-YU8_CqHe",
          '2563_2':"https://drive.google.com/uc?id=1i_WWJoRXBJPd78WFU7DXonhnuYCqTV9S",
          '2612_2':"https://drive.google.com/uc?id=1cYfg_XdDTE4UJdraBy13cr9ub-3__pX7",
          '2617_2':"https://drive.google.com/uc?id=1R3IuF1CymW6lOWMkguX0dgLWekE0Zw7S",
          '2619_4':"https://drive.google.com/uc?id=1rqVbcIQ7tZJNQ2GuEOvkWAAX8wPWRqU6",
          '2628_1':"https://drive.google.com/uc?id=1MQv_NoFNrLKBq6fai4A-t2YYNJ3Mg3LC",
          '2832_3':"https://drive.google.com/uc?id=1oyGI_GWBeS1FxWhbQXZOiHluqg-dpnKk",
          '2833_4':"https://drive.google.com/uc?id=1Bx7DMsygG842D9vFkaFCxdrexi64BC2K",
          '2837_1':"https://drive.google.com/uc?id=1zM7sx_ZtGw0G3AsSWhz2WE0B0IHEExoz",
          '2905_3':"https://drive.google.com/uc?id=16mO_AI0D8LKpBMBEeiFB8JrK8lx7J_xX",
          '2925_4':"https://drive.google.com/uc?id=1qkJ8rqg3EdcSdRYUG2zD453vUeRXoLiR",
          '2945_4':"https://drive.google.com/uc?id=1keTZ6XUmyvW1omXpfj20Ck6T4tBu4S-6",
          '2946_2':"https://drive.google.com/uc?id=18X939R_6sYguDv-9hsUwFhOMFeTTqIbj",
          '3038_6':"https://drive.google.com/uc?id=1QtVRbcCuJlaG6pvbnjkC0Eaq43jnokW-",
          '3080_2':"https://drive.google.com/uc?id=1aLTjAGFsph47AM_RluVsQSNg8V8L_Ol7",
          '3116_11':"https://drive.google.com/uc?id=1kF5UYGCM2_YLbRD302nW1ywG_BzvXxK8",
          '3132_4':"https://drive.google.com/uc?id=1mL-j71nnzptSW2Q5n8dEg7Vpc7VYXZWz",
          '3133_3':"https://drive.google.com/uc?id=1VHty1H4659XXyEo0jdbzp9D8JeQsnEMG",
          '3160_6':"https://drive.google.com/uc?id=1PCHnxuEg4aSjbPQoegQjlso9Up_xtXs2",
          '3161_4':"https://drive.google.com/uc?id=1D6huasrJiJTMhwYKNYljtEyuDjgYlmlr",
          '3550_11':"https://drive.google.com/uc?id=10k3mtKG6SOU1REMDU8EB9dNdtOr-fIBw",
          '3562_3':"https://drive.google.com/uc?id=1MHi_QNhfuDGraLeVkMxG02j8uJMPu0F6",
          '3564_1':"https://drive.google.com/uc?id=1_hAUFbxWApW_54gjMMFZgHuolUWIrceM",
          '3569_3':"https://drive.google.com/uc?id=1k0hznkxomHbm_i1YTV-SCYd96C5I_UHE",
          '3589_1':"https://drive.google.com/uc?id=1zIt0GlEfw4fEfO3iM6uOLL2P3_98TvlK",
          '3646_4':"https://drive.google.com/uc?id=1aXkYslmVlPEc2Apv6IZiGoHj_gxQ171w",
          '3718_1':"https://drive.google.com/uc?id=1W0teXVvQtJBi5dprdPbaQHcDRtGNrW6c",
          '3757_12':"https://drive.google.com/uc?id=1Gx6ciDJEFktRzgIoBa4Ew24pnlS19jOm",
          '3866_3':"https://drive.google.com/uc?id=1GXS7Uh97sZwJ6JmO954wTHv0gQZ1px2L",
          '3867_12':"https://drive.google.com/uc?id=1MsTkGIWd9qCsO3acFSTaUrk-cw-lLbcl",
          '3899_11':"https://drive.google.com/uc?id=1IUuv8xYS_XXcOMCd2xsEyqA8Jtyb9o6P",
          '3908_3':"https://drive.google.com/uc?id=1ZRk6UObuD4hPhIDkgCtsGVWBGYuxwJku",
          '3908_12':"https://drive.google.com/uc?id=187QnApOf35ZgAr0KW3RAJ2xSCqWDGLDd",
          '3979_6':"https://drive.google.com/uc?id=1lnTXsdJyxKaHIZHBluVworYCHE_5vQfs",
          '4047_6':"https://drive.google.com/uc?id=1gULvoQMaVt54j4AuURovE51IA22aaUYs",
          '4060_1':"https://drive.google.com/uc?id=1EiPn3ewSnfhbS6Wz-ufeJAM1VVsxfdKC",
          '4107_4':"https://drive.google.com/uc?id=1opoSLhxudCuKCSIvUbzff7J3VMtK9QIz",
          '4118_4':"https://drive.google.com/uc?id=17FcNmduzW2ApMoE0qmJrIQNcwYVxNS75",
          '4131_3':"https://drive.google.com/uc?id=1q8f7cgnKjeAH-XvsTp3uaT8LeFKI1UOf"}
df = pd.read_pickle(file)
df["figure"] = df.apply(lambda row:imdict[str(int(row["RUNID"])) + '_' + str(int(row['EXTID']))], axis = 1) 


for i, row in df.iterrows():    
    dictind = str(int(row["RUNID"])) + '_' + str(int(row['EXTID']))
    print 'dictind = ',dictind
    print imdict[dictind]    
    row['figure'] = imdict[dictind]
#    row['figure'] = "as;lfkdnsg"
              

#https://drive.google.com/open?id=1GXS7Uh97sZwJ6JmO954wTHv0gQZ1px2L
df.to_pickle(file)

