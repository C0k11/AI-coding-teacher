import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type Language = 'en' | 'zh'

interface LanguageState {
  language: Language
  setLanguage: (lang: Language) => void
}

export const useLanguageStore = create<LanguageState>()(
  persist(
    (set) => ({
      language: 'en',
      setLanguage: (lang) => set({ language: lang }),
    }),
    {
      name: 'language-storage',
    }
  )
)

export const translations = {
  en: {
    // Navigation
    nav: {
      home: 'Home',
      problems: 'Problems',
      battle: 'Battle',
      dashboard: 'Dashboard',
      signIn: 'Sign in',
      signOut: 'Sign out',
    },
    // Home page
    home: {
      heroTitle: 'Build your coding skills',
      heroTitleHighlight: 'with AI assistance',
      heroSubtitle: 'Algorithm practice, code analysis, real-time battles, and learning path tracking. All running locally without external APIs.',
      getStarted: 'Get started',
      codeBattle: 'Code Battle',
      stats: {
        problems: 'Problems',
        languages: 'Languages',
        battles: 'Battles',
      },
      features: {
        title: 'Core Features',
        subtitle: 'Everything you need to level up',
        description: 'A complete learning system from basic practice to competitive battles',
        problemLibrary: {
          title: 'Problem Library',
          description: '500+ curated algorithm problems covering arrays, linked lists, trees, graphs, and dynamic programming',
        },
        aiAnalysis: {
          title: 'AI Code Analysis',
          description: 'Local AI engine analyzes code quality, complexity, and algorithm patterns',
        },
        realtimeBattle: {
          title: 'Real-time Battle',
          description: '1v1 code battles with ELO rating system and global leaderboard',
        },
        learningPath: {
          title: 'Learning Path',
          description: 'Knowledge graph visualization, progress tracking, and smart recommendations',
        },
      },
      battleSection: {
        badge: 'Real-time Competition',
        title: 'Code Battle',
        description: 'Real-time 1v1 battles against players worldwide. Same problem, race to finish first. Quick match and friend challenge supported.',
        features: [
          'Real-time sync with millisecond precision',
          'ELO rating for fair matchmaking',
          'Global leaderboard',
          'Code similarity detection',
        ],
        startBattle: 'Start Battle',
        progress: 'progress',
        timeRemaining: 'Time Remaining',
      },
      cta: {
        title: 'Ready to level up your coding skills?',
        subtitle: 'Start now and let AI power your programming journey',
        getStartedFree: 'Get Started Free',
        browseProblems: 'Browse Problems',
      },
      footer: {
        about: 'About',
        docs: 'Docs',
        privacy: 'Privacy',
      },
    },
    // Login page
    login: {
      welcomeBack: 'Welcome back',
      createAccount: 'Create account',
      signInSubtitle: 'Sign in to continue your learning journey',
      signUpSubtitle: 'Register to start your coding journey',
      username: 'Username',
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      enterUsername: 'Enter username',
      enterPassword: 'Enter password',
      reEnterPassword: 'Re-enter password',
      signInBtn: 'Sign In',
      signUpBtn: 'Sign Up',
      noAccount: "Don't have an account?",
      hasAccount: 'Already have an account?',
      passwordsNoMatch: 'Passwords do not match',
      passwordTooShort: 'Password must be at least 6 characters',
      features: {
        problems: '500+ Algorithm Problems',
        battles: 'Real-time Code Battles',
        ranking: 'ELO Ranking System',
        learning: 'Learning Path Tracking',
      },
      sidebar: {
        title: 'Level up your coding skills with AI',
        subtitle: 'Algorithm problems, code battles, learning path tracking - all running locally',
      },
    },
    // Problems page
    problems: {
      title: 'Problems',
      subtitle: 'Practice algorithm problems to improve your coding skills',
      searchPlaceholder: 'Search problems...',
      allDifficulty: 'All Difficulty',
      difficulty: 'Difficulty',
      easy: 'Easy',
      medium: 'Medium',
      hard: 'Hard',
      status: 'Status',
      loading: 'Loading...',
      noProblems: 'No problems found',
    },
    // Dashboard page
    dashboard: {
      welcome: 'Welcome back',
      subtitle: 'Here is your learning progress',
      problemsSolved: 'Problems Solved',
      battlesWon: 'Battles Won',
      dayStreak: 'Day Streak',
      eloRating: 'ELO Rating',
      knowledgeGraph: 'Knowledge Graph',
      clickForDetails: 'Click node for details',
      quickActions: 'Quick Actions',
      practiceProblems: 'Practice Problems',
      codeBattle: 'Code Battle',
    },
    // Battle page
    battle: {
      title: 'Code Battle',
      subtitle: 'Compete with players worldwide on the same problem',
      selectMode: 'Select Battle Mode',
      quickBattle: {
        name: 'Quick Battle',
        description: 'Fill-in-the-blank & multiple choice code questions',
      },
      codeBattle: {
        name: 'Code Battle',
        description: 'Race to solve a coding problem 1v1',
      },
      friendChallenge: {
        name: 'Friend Challenge',
        description: 'Challenge a friend to a code battle',
      },
      friendUsername: 'Friend Username',
      enterFriendUsername: "Enter friend's username",
      startBattle: 'Start Battle',
      matching: 'Matching...',
      timeLimit: 'Time Limit',
      questions: 'Questions',
      battleMode: 'Battle Mode',
      maxPoints: 'Max Points',
    },
    // Problem description
    problemDesc: {
      examples: 'Examples',
      input: 'Input:',
      output: 'Output:',
      explanation: 'Explanation:',
      constraints: 'Constraints',
      hints: 'Hints',
      getNextHint: 'Get Next Hint',
      loadingHint: 'Loading...',
      solutions: 'Solutions',
      time: 'Time:',
      space: 'Space:',
    },
    // Common
    common: {
      developer: 'Developer',
    },
  },
  zh: {
    // Navigation
    nav: {
      home: '首页',
      problems: '题库',
      battle: '对战',
      dashboard: '仪表盘',
      signIn: '登录',
      signOut: '退出',
    },
    // Home page
    home: {
      heroTitle: '提升你的编程技能',
      heroTitleHighlight: '借助AI助手',
      heroSubtitle: '算法练习、代码分析、实时对战和学习路径追踪。完全本地运行，无需外部API。',
      getStarted: '开始学习',
      codeBattle: '代码对战',
      stats: {
        problems: '题目',
        languages: '语言',
        battles: '对战',
      },
      features: {
        title: '核心功能',
        subtitle: '全方位提升你的编程能力',
        description: '从基础练习到竞技对战的完整学习体系',
        problemLibrary: {
          title: '题目库',
          description: '500+精选算法题目，涵盖数组、链表、树、图和动态规划',
        },
        aiAnalysis: {
          title: 'AI代码分析',
          description: '本地AI引擎分析代码质量、复杂度和算法模式',
        },
        realtimeBattle: {
          title: '实时对战',
          description: '1v1代码对战，ELO评分系统和全球排行榜',
        },
        learningPath: {
          title: '学习路径',
          description: '知识图谱可视化、进度追踪和智能推荐',
        },
      },
      battleSection: {
        badge: '实时竞技',
        title: '代码对战',
        description: '与全球玩家实时1v1对战。相同题目，竞速完成。支持快速匹配和好友挑战。',
        features: [
          '毫秒级精度实时同步',
          'ELO评分公平匹配',
          '全球排行榜',
          '代码相似度检测',
        ],
        startBattle: '开始对战',
        progress: '进度',
        timeRemaining: '剩余时间',
      },
      cta: {
        title: '准备好提升你的编程技能了吗？',
        subtitle: '立即开始，让AI助力你的编程之旅',
        getStartedFree: '免费开始',
        browseProblems: '浏览题库',
      },
      footer: {
        about: '关于',
        docs: '文档',
        privacy: '隐私',
      },
    },
    // Login page
    login: {
      welcomeBack: '欢迎回来',
      createAccount: '创建账号',
      signInSubtitle: '登录以继续你的学习之旅',
      signUpSubtitle: '注册以开启你的编程之旅',
      username: '用户名',
      email: '邮箱',
      password: '密码',
      confirmPassword: '确认密码',
      enterUsername: '请输入用户名',
      enterPassword: '请输入密码',
      reEnterPassword: '请再次输入密码',
      signInBtn: '登录',
      signUpBtn: '注册',
      noAccount: '还没有账号？',
      hasAccount: '已有账号？',
      passwordsNoMatch: '两次密码不一致',
      passwordTooShort: '密码至少6个字符',
      features: {
        problems: '500+算法题目',
        battles: '实时代码对战',
        ranking: 'ELO排名系统',
        learning: '学习路径追踪',
      },
      sidebar: {
        title: '借助AI提升你的编程技能',
        subtitle: '算法题目、代码对战、学习路径追踪 - 完全本地运行',
      },
    },
    // Problems page
    problems: {
      title: '题库',
      subtitle: '通过练习算法题目来提升你的编程技能',
      searchPlaceholder: '搜索题目...',
      allDifficulty: '全部难度',
      difficulty: '难度',
      easy: '简单',
      medium: '中等',
      hard: '困难',
      status: '状态',
      loading: '加载中...',
      noProblems: '未找到题目',
    },
    // Dashboard page
    dashboard: {
      welcome: '欢迎回来',
      subtitle: '这是你的学习进度',
      problemsSolved: '已解题目',
      battlesWon: '对战胜利',
      dayStreak: '连续天数',
      eloRating: 'ELO评分',
      knowledgeGraph: '知识图谱',
      clickForDetails: '点击节点查看详情',
      quickActions: '快捷操作',
      practiceProblems: '练习题目',
      codeBattle: '代码对战',
    },
    // Battle page
    battle: {
      title: '代码对战',
      subtitle: '与全球玩家在同一题目上竞技',
      selectMode: '选择对战模式',
      quickBattle: {
        name: '快速对战',
        description: '填空题和代码选择题',
      },
      codeBattle: {
        name: '代码对战',
        description: '1v1竞速解决编程问题',
      },
      friendChallenge: {
        name: '好友挑战',
        description: '向好友发起代码对战挑战',
      },
      friendUsername: '好友用户名',
      enterFriendUsername: '输入好友的用户名',
      startBattle: '开始对战',
      matching: '匹配中...',
      timeLimit: '时间限制',
      questions: '题目数',
      battleMode: '对战模式',
      maxPoints: '最高分数',
    },
    // Problem description
    problemDesc: {
      examples: '示例',
      input: '输入：',
      output: '输出：',
      explanation: '解释：',
      constraints: '约束条件',
      hints: '提示',
      getNextHint: '获取下一个提示',
      loadingHint: '加载中...',
      solutions: '题解',
      time: '时间：',
      space: '空间：',
    },
    // Common
    common: {
      developer: '开发者',
    },
  },
}

export type Translations = typeof translations.en

export function useTranslations() {
  const { language } = useLanguageStore()
  return translations[language]
}
