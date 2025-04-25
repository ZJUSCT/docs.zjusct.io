# 竞赛

本文档仅用于存放竞赛赛题、赛程、排名等信息，**赛题解答等技术资料不对外公开，见内部文档**。

## 时间轴

::gantt:: no-weeks month-width=50 month-format="%b"
[
    {
        "title": "ISC25",
        "activities": [
            {
                "title": "Virtual Opening Ceremony",
                "start": "2025-04-01",
                "end": "2025-04-01"
            },
            {
                "title": "Virtual Competition Ends",
                "start": "2025-05-09",
                "end": "2025-05-09"
            },
            {
                "title": "Virtual Team Interviews",
                "start": "2025-05-12",
                "end": "2025-05-23"
            },
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
        "title": "ASC25",
        "activities": [
            {
                "title": "Preliminary Competition",
                "start": "2025-01-06",
                "end": "2025-02-21"
            },
            {
                "title": "Final Competition",
                "start": "2025-05-10",
                "end": "2025-05-14"
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
