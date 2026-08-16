# SG Student Event Radar

给新加坡留学生用的活动搜索 Skill。

它会按照你关注的行业、岗位、公司、技能、预算和空闲时间，搜索新加坡近期活动，去重并核验信息，再留下少量值得你看的候选。

适合这样的情况：

- 活动散落在学校网站、公司官网、Luma、Eventbrite 和 Meetup；
- 群里看到活动时，报名可能已经结束；
- 不想每天重复搜索和判断活动是否值得参加；
- 希望活动能真正服务于行业探索、实习求职、项目或学术目标。

## 它怎么工作

```text
读取你的目标和时间限制
  → 搜索通用平台与行业来源
  → 在抓取详情前去重
  → 核验时间、地点、价格和报名状态
  → 根据个人目标评分
  → 输出每日少量候选
  → 你用 5 分钟选择：想参加 / 暂时保留 / 不感兴趣
```

你可以把它设置成晚上运行，第二天只看筛选结果。选择“想参加”后，代理会建议一个具体准备动作，例如研究一位嘉宾或准备两个问题。

它不会自动报名、付款、发消息、添加日历或邀请别人。任何外部操作都需要你在执行时确认。

## 适用人群

- Polytechnic、本科、硕士和博士留学生；
- 正在探索行业、找实习、准备全职求职的人；
- 想通过工作坊、比赛、行业交流或项目活动积累经历的人；
- 金融、咨询、医疗、消费品、科技、可持续发展等方向均可自行配置。

## 安装

需要一个可以读取 Skill、浏览网页并运行 Python 3 的 AI 代理环境。

```bash
git clone https://github.com/wendy200210/sg-student-event-radar.git
cd sg-student-event-radar
python3 scripts/init_local_state.py
```

如果使用 Codex，可把仓库注册到 Skills 目录：

```bash
ln -s "$(pwd)" ~/.codex/skills/sg-student-event-radar
```

重新打开任务后，可以直接说：

```text
使用 $sg-student-event-radar 帮我完成首次配置。
```

也可以在终端运行配置向导：

```bash
python3 scripts/configure_profile.py
python3 scripts/validate_config.py
```

配置和历史记录只保存在被 Git 忽略的 `local/` 目录。

## 你可以设置什么

- 学历阶段和预计毕业时间；
- 正在探索的 1 至 5 个行业；
- 目标岗位、公司、技能和活动目的；
- 不想看到的主题；
- 预算、语言、地点和线上活动偏好；
- 上课时间、固定安排和考试周；
- 每天最多查看几个活动。

示例：

```json
{
  "student_profile": {
    "education_stage": "master",
    "graduation_date": "2027-06",
    "career_stage": ["internship", "industry exploration"]
  },
  "focus": {
    "industries": ["financial services"],
    "fields": ["risk", "asset management"],
    "target_roles": ["risk analyst"],
    "goals": ["job access", "industry understanding"]
  }
}
```

完整字段见 [`config.example.json`](config.example.json)。请把个人内容写入 `local/config.json`，不要修改后直接公开示例文件。

## 运行一次扫描

在支持 Skill 的代理中说：

```text
使用 $sg-student-event-radar 扫描未来 45 天适合我的新加坡活动。
```

代理会完整读取 [`routine-prompt.md`](routine-prompt.md)，并按其中的去重、核验、评分和报告规则运行。

默认结果保存在本地。每天的私有报告位于 `reports/YYYY-MM-DD.md`，历史和选择记录位于 `local/ledger.json`。

## 设置夜间自动运行

在支持定时任务的代理中，创建一个每日任务，并让它：

```text
进入 sg-student-event-radar 仓库，完整读取 routine-prompt.md，然后执行活动扫描。
时区使用 Asia/Singapore。
```

建议安排在晚上，第二天只处理少量候选。定时任务是否能访问网页和 Notion，取决于你的代理环境和连接状态。

## Notion 是可选的

没有 Notion 也能完整运行。

如果已经连接 Notion，可以让代理按照 [`references/notion-schema.md`](references/notion-schema.md) 创建或复用活动数据库。数据库 ID 只能保存在 `local/notion-state.json`，不能提交到公开仓库。

Notion 中只需要维护三个选择：

- `Interested`
- `Considering`
- `Not interested`

同步时，代理不得覆盖你的选择。Notion 暂时不可用时，结果仍会保存在本地，等待之后补同步。

## 推荐依据

每个活动按 10 分制评估：

- 与当前目标的相关性：3 分；
- 能接触到的人：2 分；
- 能形成的具体成果：2 分；
- 学生是否容易参加：1 分；
- 时间、地点和价格是否可行：2 分。

免费、热门或主办方有名不会自动获得高分。完整规则见 [`references/scoring-rubric.md`](references/scoring-rubric.md)。

## 隐私和发布检查

以下内容不会进入版本控制：

- 个人目标和课表；
- Notion 数据库 ID；
- 活动历史和个人选择；
- 每日扫描报告。

公开发布前运行：

```bash
python3 scripts/check_public_release.py
```

如果发现私有状态、Notion 标识、疑似密钥或未提交的公开修改，检查会失败。

## English

SG Student Event Radar is an open-source agent skill for international students in Singapore. It discovers events across user-selected industries, verifies key details, removes duplicates, scores each event against the student's goals and schedule, and creates a small daily review queue.

The workflow supports any field, keeps personal state out of Git, works without Notion, and never registers, pays, messages, or creates external invitations without confirmation.

Start with:

```bash
git clone https://github.com/wendy200210/sg-student-event-radar.git
cd sg-student-event-radar
python3 scripts/init_local_state.py
python3 scripts/configure_profile.py
python3 scripts/validate_config.py
```

Then ask a compatible agent to use `$sg-student-event-radar` and run the complete protocol in `routine-prompt.md`.

## License

[MIT](LICENSE)
