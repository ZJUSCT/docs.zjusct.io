# 竞赛

本文档仅用于存放竞赛赛题、赛程、排名等信息，**赛题解答等技术资料不对外公开，见内部文档**。

## 时间轴

::gantt:: no-weeks month-width=50 month-format="%b"
[
    {
        "title": "ISC25",
        "activities": [
            {
                "title": "In-Person Opening Ceremony",
                "start": "2025-06-10",
                "end": "2025-06-10"
            },
            {
                "title": "Award Ceremony",
                "start": "2025-06-12",
                "end": "2025-06-12"
            }
        ]
    },
    {
        "title": "SCC & IndySCC",
        "activities": [
            {
                "title": "Getting Started 研讨会",
                "start": "2025-04-07",
                "end": "2025-04-07"
            },
            {
                "title": "IndySCC 申请开放",
                "start": "2025-03-01",
                "end": "2025-03-01"
            },
            {
                "title": "IndySCC 申请截止",
                "start": "2025-05-16",
                "end": "2025-05-16"
            },
            {
                "title": "IndySCC 通知发送",
                "start": "2025-06-16",
                "end": "2025-06-16"
            },
            {
                "title": "IndySCC 比赛",
                "start": "2025-11-17",
                "end": "2025-11-19"
            }
        ]
    },
    {
        "title": "PAC 2025",
        "activities": [
            {
                "title": "报名截止 & 初赛赛题发布",
                "start": "2025-06-15",
                "end": "2025-06-15"
            },
            {
                "title": "初赛截止日期",
                "start": "2025-07-01",
                "end": "2025-07-01"
            },
            {
                "title": "决赛任务发布",
                "start": "2025-07-15",
                "end": "2025-07-15"
            },
            {
                "title": "决赛提交截止",
                "start": "2025-08-15",
                "end": "2025-08-15"
            }
        ]
    },
    {
        "title": "SolverChallenge25",
        "activities": [
            {
                "title": "任务公布",
                "start": "2025-05-15",
                "end": "2025-05-15"
            },
            {
                "title": "报名截止",
                "start": "2025-06-15",
                "end": "2025-06-15"
            },
            {
                "title": "提交截止",
                "start": "2025-07-15",
                "end": "2025-07-15"
            },
            {
                "title": "答辩和颁奖",
                "start": "2025-08-02",
                "end": "2025-08-02"
            }
        ]
    }
]
::/gantt::

## 竞赛排名

HPC Advisory Council 维护了全球高校在三大超算竞赛的排名，见 [Worldwide Leadership List - HPC Advisory Council](https://www.hpcadvisorycouncil.com/worldwide-leadership-list.php)。

<iframe src="https://www.hpcadvisorycouncil.com/worldwide-leadership-list-frame.html" width="100%" height="600" frameborder="0"></iframe>

## 竞赛总览

超算相关的竞赛一般作为大型会议的一个子项目存在。比如著名的 ASC、ISC、SCC 竞赛分别对应亚洲、欧洲、美洲的超算会议，SolverChallenge（第四届线性解法器算法与性能优化竞赛）是解法器快速算法及应用研讨会（SOLVER 会议）的活动等。

### SCC 与 IndySCC

[SC Conference](https://supercomputing.org/) 是美洲最大的高性能计算会议，每年 11 月在美国举办。

该会议下设两个学生竞赛项目：

!!! note "Student Cluster Competition (SCC)"

    > With sponsorship from hardware and software vendor partners, competing student teams design and build small clusters, learn scientific applications, and apply optimization techniques for their chosen architectures in a non-stop, 48-hour challenge.

    [SCC](https://www.studentclustercompetition.us/index.html) 是一个 48 小时的比赛，参赛队伍需要在比赛现场组装一台小型超算，并在比赛期间运行一些科学应用程序，最终获得最高的性能。

!!! note "IndySCC"

    > The IndySCC is an event sharing the goals of the SCC but with an emphasis on education and inclusion, intended for **less-experienced teams**. Teams compete remotely using provided hardware through an education-focused experience supported by HPC industry experts **during the months leading up to the conference**. A **48-hour contest the weekend prior to SC** will be the culmination of the experience and knowledge gained by the teams in the preceding months.

    IndySCC 是 SCC 的简单版本。参赛队伍在比赛前几个月通过远程访问提供的硬件进行学习，最后会有一个 48 小时的比赛作为前几个月的学习总结。

#### IndySCC 24

[Student Cluster Competition • SC24](https://sc24.supercomputing.org/students/student-cluster-competition/)

- [scc24-hpl.pdf](scc24-hpl.pdf)
- [scc24-icon.pdf](scc24-icon.pdf)
- [scc24-mystery.pdf](scc24-mystery.pdf)
- [scc24-namd.pdf](scc24-namd.pdf)

### ISC SCC

[International Supercomputing Conference](https://www.isc-hpc.com/) 是欧洲最大的高性能计算会议，每年 5-6 月在欧洲举办。

该会议下设一个学生竞赛项目：

!!! note "ISC SCC"

    > The ISC Student Cluster Competition encourages international teams of university students to showcase their expertise in a friendly yet spirited competition that fosters critical skills, professional relationships, competitive spirit and lifelong comraderies.
    >
    > The Competition is an integral part of the ISC event and ongoing success and growing recognition as a world championship competition are a result of the collaborative partnership between ISC and the HPC-AI Advisory Council.
    >
    > The **virtual part** will be open for all teams, the teams will be connecting to remote clusters and run HPC applications, performing benchmarks and participate in the given challenges.
    >
    > The **in-person part** will be open for up to seven teams. The onsite teams will bring and assemble their own cluster, and run the micro-benchmarks and HPC applications, within three days of the ISC High Performance Conference.

    ISC SCC 分为 Virtual Part 和 In-Persion Part。目前我们参加的是 Virtual Part，有大约一个月的时间远程访问提供的硬件进行学习。

ISC SCC 赛题有官方在线存档，因此这里不再留档。

#### ISC SCC 25

[ISC25 SCC - Virtual Part - HPC-Works - Confluence](https://hpcadvisorycouncil.atlassian.net/wiki/spaces/HPCWORKS/pages/3177283633/ISC25+SCC+-+Virtual+Part)

#### ISC SCC 24

[ISC24 SCC - Virtual Part - HPC-Works - Confluence](https://hpcadvisorycouncil.atlassian.net/wiki/spaces/HPCWORKS/pages/3017113601/ISC24+SCC+-+Virtual+Part)

### ASC

[Asia Supercomputer Community (ASC)](http://www.asc-events.org/) 是亚洲超算社区，每年 4-5 月在中国举办一次学生竞赛。

- 每个学校派出多支队伍参赛，每支队伍 5 名本科生和 1 位指导老师。
- 每个学校最多一支队伍进入决赛。
- 决赛赛题一般包含：benchmark、应用调优、团队赛题、e Prize。

#### ASC 25

- [asc25-pre-round](asc25-pre-round.pdf)

#### ASC 24

[ASC24 Final](http://www.asc-events.org/StudentChallenge/History/2024/index.html)

- [asc24-group](asc24-group.pdf)

### PAC

> 全国并行应用挑战赛 ParallelApplicationChallenge（以下简称“竞赛”或者“PAC”）由全国信标委算力标准工作组指导，ACM 中国高性能计算专家委员会和中国智能计算产业联盟主办。竞赛自 2013 年创办以来，获得了清华大学、北京大学、中国科学技术大学、山东大学、中国科学院等国内知名高校、科研单位的参赛支持。现已逐渐发展为国内（含港澳台）影响力最大的并行计算赛事之⼀。

PAC 一般在每年 6-8 月举行，分为“并行优化赛道”和“并行应用赛道”两个赛道，我们一般参加“并行优化赛道”。

#### PAC 2025

- [赛事链接](http://www.paratera-edu.org.cn/enterstep/index?id=12&groupTag=PAC)
- 报名截止日期 & 初赛赛题发布：2025-06-15
- 初赛截止日期：2025-07-01
- 决赛任务发布：2025-07-15
- 决赛提交截止：2025-08-15

### SolverChallenge

> SolverChallenge 竞赛是解法器快速算法及应用研讨会（SOLVER 会议）的一项特色活动，由 SOLVER 会议组委会主办，每年举行一次。竞赛针对实际应用中抽取出来的线性代数问题，要求参赛队伍在一定约束条件下通过算法设计与性能调优等手段对这些系统进行数值求解，并基于不同标准从多个维度对所获结果进行评价。

SolverChallenge 一般在 6-7 月份举行，赛题主要是在给定平台上对 10 个线性系统进行求解，以正确性和速度计算得分。

#### SolverChallenge25

- [赛事链接](https://www.solver-conference.cn/solverchallenge25/)
- 任务公布：2025-05-15
- 报名截止：2025-06-15
- 提交截止：2025-07-15
- 答辩和颁奖：2025-08-02
