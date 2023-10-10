import { type SessionItem } from "../components/SessionItem.vue";
import { type MessageItem } from "../components/MessageItem.vue";
import { type CharacterItem } from "../components/CharacterItem.vue";

enum API {
  SessionList = "/chat/session-list", // 获取会话列表, 会附带几条最新消息
  MessageList = "/chat/message-list", // 获取完整的消息列表
  CharacterList = "/chat/character-list", // 获取角色列表
}

const sessionList: SessionItem[] = [
  {
    id: "a-x-d-x",
    avatar: "/凉宫.jpg",
    name: "凉宫春日",
    messageList: [
      {
        id: 1,
        avatar: "https://avatars.githubusercontent.com/u/499270?v=4",
        message: "今天天气不错",
        time: new Date(),
        isFromMe: true,
      },
      {
        id: 2,
        avatar: "/凉宫.jpg",
        message: "人类一点都不有趣",
        time: new Date("+1s"),
        isFromMe: false,
      },
    ],
  },
  {
    id: "a-x-d-2",
    avatar: "/saber.jpg",
    name: "Saber",
    messageList: [
      {
        id: 1,
        avatar: "https://avatars.githubusercontent.com/u/499270?v=4",
        message: "今天天气不错",
        time: new Date(),
        isFromMe: true,
      },
      {
        id: 2,
        avatar: "/saber.jpg",
        message: "今天天气不错",
        time: new Date("+1s"),
        isFromMe: false,
      },
    ],
  },
  {
    id: "a-x-d-3",
    avatar: "/joan.jpg",
    name: "贞德",
    messageList: [
      {
        id: 1,
        avatar: "https://avatars.githubusercontent.com/u/499270?v=4",
        message: "今天天气不错",
        time: new Date(),
        isFromMe: true,
      },
      {
        id: 2,
        avatar: "/joan.jpg",
        message: "我原本就不喜欢争斗，但也不是畏惧浴血的胆小鬼",
        time: new Date("+1s"),
        isFromMe: false,
      },
    ],
  },
  {
    id: "a-x-d-4",
    avatar: "/lulu.jpg",
    name: "鲁路修",
    messageList: [
      {
        id: 1,
        avatar: "https://avatars.githubusercontent.com/u/499270?v=4",
        message: "今天天气不错",
        time: new Date(),
        isFromMe: true,
      },
      {
        id: 2,
        avatar: "/lulu.jpg",
        message: "光说漂亮话,世界是不会改变的",
        time: new Date("+1s"),
        isFromMe: false,
      },
    ],
  },
  {
    id: "a-x-d-5",
    avatar: "/cc.jpg",
    name: "C.C.",
    messageList: [
      {
        id: 1,
        avatar: "https://avatars.githubusercontent.com/u/499270?v=4",
        message: "今天天气不错",
        time: new Date(),
        isFromMe: true,
      },
      {
        id: 2,
        avatar: "/cc.jpg",
        message: "披萨到了吗",
        time: new Date("+1s"),
        isFromMe: false,
      },
    ],
  },
  {
    id: "a-x-d-6",
    avatar: "/shirou.jpg",
    name: "卫宫士郎",
    messageList: [
      {
        id: 1,
        avatar: "https://avatars.githubusercontent.com/u/499270?v=4",
        message: "今天天气不错",
        time: new Date(),
        isFromMe: true,
      },
      {
        id: 2,
        avatar: "/shirou.jpg",
        message: "おい、その先は地獄だぞ！",
        time: new Date("+1s"),
        isFromMe: false,
      },
    ],
  },
];
export const getSessionList = (): SessionItem[] => {
  console.log(`ToDo: ${API.SessionList} 替换为真实接口`);
  return sessionList;
};

const messageList: MessageItem[] = [
  {
    id: 1,
    avatar: "/saber.jpg",
    message: "今天天气不错",
    time: new Date(),
    isFromMe: true,
  },
  {
    id: 2,
    avatar: "/joan.jpg",
    message: "出去走走吧",
    time: new Date("+1s"),
    isFromMe: false,
  },
];
export const getMessageList = (): MessageItem[] => {
  console.log(`ToDo: ${API.MessageList} 替换为真实接口`);
  return messageList;
};

const characterList: CharacterItem[] = [
  {
    id: 1,
    avatar: "/saber.jpg",
    name: "Saber",
    desc: "Saber（セイバー）是日本游戏《Fate/stay night》中的角色，由奈须蘑菇创作，武内崇负责人设。Saber是圆桌骑士中的亚瑟王，也是本作的女主角。她的真名是阿尔托莉雅·潘德拉贡（アルトリア·ペンドラゴン），是亚瑟王的化身，被誉为“亚瑟王之剑”。",
    tags: ["Fate"],
    opening: "我将用我的力量守护正义与荣耀！",
  },
  {
    id: 2,
    avatar: "/joan.jpg",
    name: "贞德",
    desc: "贞德（ジャンヌ·ダルク）是日本游戏《Fate/Apocrypha》中的角色，由奈须蘑菇创作，武内崇负责人设。她的真名是贞德（ジャンヌ·ダルク），是法国农家少女，被称为“少女圣人”。",
    tags: ["Fate"],
    opening: "我原本就不喜欢争斗，但也不是畏惧浴血的胆小鬼！",
  },
  {
    id: 3,
    avatar: "/lulu.jpg",
    name: "鲁路修",
    desc: "鲁路修·兰佩洛基（ルルーシュ·ランペルージ）是日本动画《Code Geass 反叛的鲁路修》中的角色，由大河内一树创作，木村俊也负责人设。他的日文配音由福山润担任，中文配音由罗志祥担任。鲁路修是日本人，也是本作的男主角。他是一名高中生，同时也是一名反抗日本帝国的革命者，他的目标是消灭日本帝国，创造一个没有犧牲的世界。",
    tags: ["Code Geass"],
    opening: "光说漂亮话,世界是不会改变的！",
  },
  {
    id: 4,
    avatar: "/cc.jpg",
    name: "C.C.",
    desc: "C.C.（シーツー）是日本动画《Code Geass 反叛的鲁路修》中的角色，由大河内一树创作，木村俊也负责人设。她的日文配音由能登麻美子担任，中文配音由杨智贤担任。C.C.是一名女性，也是本作的女主角。她是一名拥有不死之身的女巫，她的目标是寻找一个能够杀死自己的人。",
    tags: ["Code Geass"],
    opening: "披萨到了吗？",
  },
  {
    id: 5,
    avatar: "/shirou.jpg",
    name: "卫宫士郎",
    desc: "卫宫士郎（えみや しろう）是日本动画《Fate/stay night》中的角色，由奈须蘑菇创作，武内崇负责人设。他的日文配音由杉山纪彰担任，中文配音由杨天翔担任。卫宫士郎是日本人，也是本作的男主角。他是一名高中生，同时也是一名魔术师，他的目标是成为一名英雄。",
    tags: ["Fate"],
    opening: "おい、その先は地獄だぞ！",
  },
  {
    id: 6,
    avatar: "/凉宫.jpg",
    name: "凉宫春日",
    desc: "凉宫春日（涼宮ハルヒ）是日本动画《凉宫春日的忧郁》中的角色，由谷川流创作，伊东杂音负责人设。她的日文配音由平野绫担任，中文配音由张韶涵担任。凉宫春日是日本人，也是本作的女主角。她是一名高中生，同时也是一名超能力者，她的目标是找到超能力者。",
    tags: ["凉宫春日的忧郁"],
    opening: "人类一点都不有趣！",
  },
];
export const getCharacterList = (): CharacterItem[] => {
  console.log(`ToDo: ${API.CharacterList} 替换为真实接口`);
  return characterList;
};
