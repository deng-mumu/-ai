  应用背景：很多人都是没有一个能够陪伴聊天的人，而且目前大环境下压力很大，很多人都是一个人在大城市打拼，下班回家都没有一个可以陪伴说话的人。当下也存在着大量的空巢老人，为此制作了虚拟聊天助手。解决了年轻人的内心的空虚，也可以陪伴独居的老人，可以进行情感的交流，释放内心的压力。减少心理问题。

        有了希望解决的问题，那么我们就需要思考大框架，首先必须要能够普通定制，每个人都能拥有自己想要的角色，所以收集需要扮演的角色，例如：男朋友，女朋友等不同的角色。另外也要给予一个角色的姓名和特点，这样才能使得ai有比较好的表现，同时也增加了带入感。

        所以就需要有能够收集信息的ai助手。收集到信息之后就要构建prompt，构建了prompt就确定了system。之后就可以利用ChatTTS将输出的文字用语音输出。

        （刚刚的是普通定制就只是利用ai原本的能力，那么高级定制就可以利用微调技术，生成具有更符合用户特点的输出）以下都是普通定制内容，这里只是提供微调的想法，但是未实现。

        ChatTTS是输入文字，输出语音，AI能生成逼真的中英文语音和语气。作为数字人、大模型、人机对话、具身智能的语音交互基座。
        ​
     
       streamlit run demo.py运行的效果，chattts的语音生成有点慢

![43a111a3eb244a829a0e2d1b27bf2581](https://github.com/user-attachments/assets/ca20604c-5e9a-40eb-87bf-d1108264088d)
    如果你想改人物只需要在修改demo输入yes就可以更改了 （目前每次打开只能重新生成一次，不能重复改），想要再次修改只能重启demo

 ![acc83ac5f2894210aec761b11c91f359](https://github.com/user-attachments/assets/316b919f-f952-481e-b467-d55633f63d11)
![6d7f69f0942944c8bffbc95d0e3e174c](https://github.com/user-attachments/assets/ada6fb26-122f-41d7-a6cb-287a7bc791e2)
 大概流程就是这样，目前任在优化中，待续...
