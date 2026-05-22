Q/CIB
兴业银行股份有限公司企业标准
Q/CIB 4052.1—2024


公共技术服务接入操作程序 第1部分：
技术中台缓存服务接入手册
Public technical service access operation procedures—Part 1:
technical central platform cache service access handbook

2024-10-30发布
2024-10-30实施
兴业银行股份有限公司发布
ICS 35.240.40
CCS A 11


目  次
目次	Ⅰ
前言	Ⅲ
1 范围	1
2 规范性引用文件	1
3 术语和定义	1
4 缩略语	2
5 基本概念	3
5.1 部署模式	3
5.2 持久化模式	3
5.3 缓存数据结构	3
5.4 缓存数据淘汰策略	4
6 缓存服务	4
6.1 服务特点	4
6.2 服务模式	5
6.3 服务容灾	5
7 设计指引	5
7.1 缓存依赖	5
7.2 数据隔离	5
7.3 部署模式	6
7.4 部署区域	7
7.5 功能接口	7
7.6 缓存数据结构	8
7.7 容灾功能	8
8 开发指引	9
8.1 服务端版本要求	9
8.2 客户端版本要求	9
8.3 客户端配置	10
8.4 命令使用说明	16
8.5 容错开发说明	18
8.6 容灾开发说明	18
8.7 安全编码	19
9 测试指引	19
9.1 性能测试	19
9.2 专项测试	19
10 上线指引	20
10.1 前置资源准备	20
10.2 告警规则确认	20
10.3 接入前置检查	20
10.4 应急卡片准备	20
附录A（规范性） 指导文件	21

前  言
本文件按照GB/T 1.1—2020《标准化工作导则 第1部分：标准化文件的结构和起草规则》给出的规则起草。
本文件由兴业银行科技管理部提出并归口。
本文件起草单位：兴业数字金融服务（上海）股份有限公司。
本文件主要起草人：林鑫、王畅。
本文件为首次发布。
公共技术服务接入操作程序
第1部分：技术中台缓存服务接入手册
范围
本文件给出了接入系统使用缓存服务时应遵循的设计原则、编码规范、测试要求，引导接入系统合理、高效地使用公共技术服务，提升应用的稳定性与可维护性。
本文件适用于全集团具有研发、运维职能的单位。
规范性引用文件
本文件没有规范性引用文件。
术语和定义

技术中台  technical middle office
将本行公共的、通用的关键基础技术资源集中建设和维护，以平台形式提供技术服务。
技术中台包括应用开发平台、Devops与研发保障、应用集成、微服务支撑与治理、数字化运营与支撑、通用技术服务、基础PaaS、容器云平台八大板块。

技术中台缓存（Redis）服务  technical middle office in-memory(Redis) Service
缓存服务
技术中台基于云原生Operator技术，将Redis软件实现PaaS化，并作为一类基础技术服务进行提供，具备按需申请、快速交付、局部故障自愈和高可用性等特性。
根据JR/T 0166—2020定义，PaaS（platform as a Service，平台即服务）为云服务类别中的一种。
Operator是一种用于管理Kubernetes集群中复杂应用的工具，基于Kubernetes的控制器，自动化复杂应用的部署、管理和运维过程。

Redis实时数据平台  Redis real-time data platform
Redis
一种开源的内存数据存储中间件，最常用于缓存场景，支持高速读写、发布订阅和事务处理等功能，支持多种数据结构，具备高可用性、可扩展性和高性能等特点。
来源自Redis第三方开源运营网址，https://redis.io，相关定义有修改。

键值  key and value
Key/Value
Redis提供的数据存储结构，其中Key是用于在Redis中唯一标识存储数据的字符串，而Value是与Key相关联的数据信息；键值结构支持包括字符串、哈希、列表、集合在内的多种数据类型。

Redis代理  Redis Proxy
Proxy
一种高性能的负载均衡组件，基于Redis协议实现，用于应用程序到Redis集群的路由代理，具备高性能、高可用性和低耦合等特点，在Redis跨机房部署时用于流量路由和容灾网关。

Redis发布/订阅  Redis Pub/Sub
Pub/Sub
Redis提供的一种消息通信模式，允许发送者将消息发送到Redis指定的频道（channel），接收者可通过订阅channel来接收消息，提供轻量级通知功能。

全量持久化  Redis Database Backup
RDB
Redis提供的一种全量数据持久化存储能力。使用RDB持久化时，可定时将内存中的数据全量存储到磁盘文件中。

增量持久化  Append-Only File
AOF
Redis提供的一种增量数据持久化存储能力。使用AOF持久化时，可定时地将内存数据的增量变更存储到磁盘文件中。
缩略语
下列缩略语适用于本文件。
TPS：每秒事务处理数（Transactions Per Second）
VIP：虚拟IP地址（Virtual IP）
TTL：数据存活时间（Time To Live）
JSON：JS对象简谱（JavaScript Object Notation）
XML：可扩展标记语言（eXtensible Markup Language）
DNS：域名系统（Domain Name System）
基本概念
部署模式
Redis作为内存数据存储中间件，提供单点模式、主从模式、哨兵模式和分片集群模式四种不同的部署模式，接入系统可根据应用可用性要求和数据量处理要求选择，具体可见表1。
表1  部署模式分类
持久化模式
Redis作为内存数据存储中间件，本身在数据一致性、可靠性、事务能力等方面与传统数据库（MySQL、Oracle等）存在明显差异，接入系统可根据性能、持久化等要求综合考虑，结合Redis存储模式特点进行选择，具体可见表2。
表2  持久化模式分类
缓存数据结构
Redis支持多种数据结构，接入系统可根据每类数据结构特点和应用场景，在使用中选择合适的数据结构，具体可见表3。
表3  缓存数据结构说明
缓存数据淘汰策略
Redis作为内存型中间件，数据存储于内存是其主要特点，提供了内存使用限制和淘汰策略来优化内存使用，接入系统可根据实际情况进行相关参数配置，具体可见表4。
表4  缓存数据淘汰策略说明
缓存服务
服务特点
缓存服务提供了高效管理缓存实例生命周期的能力，可快速部署、配置、管理Redis服务实例，接入系统无需关注底层部署服务器资源及技术细节，应重点关注如何正确、合理地使用缓存能力，当前缓存服务具备以下特性。
多模式支持：支持主从模式、集群模式，满足不同业务场景需求。
信创适配：支持鲲鹏、海光芯片、麒麟操作系统，具备全栈信创支持能力。
局部故障自愈：可在服务器宕机等异常场景时，自动恢复、重启Redis服务，尽量减少故障影响。
高可用切换：主从模式、集群模式下当因网络异常、服务器异常引起部分Redis节点异常时，可自动进行主从切换，配合应用客户端重试重连配置，提升业务连续性保障。
服务模式
缓存服务当前提供两种部署模式：Redis主从模式、Redis集群模式，均支持数据备份和故障场景下高可用切换，接入系统应根据两类模式特点，结合业务需求进行选择。
缓存服务主从模式：
基于Redis主从及哨兵模式提供服务，默认配置为1个主节点和1个从节点以及3个哨兵节点，接入系统应根据实际需求调整从节点数；
推荐用于小规模应用，在该模式下采用VIP路由机制，接入系统应在客户端配置单个VIP地址，异常情况下VIP机制会在Redis主从切换后自动指向新的Redis主节点；
主从切换时，接入系统不必调整客户端配置地址。
缓存服务集群模式：
基于Redis集群模式提供服务，默认提供三个分片，每个分片配置为1个主节点和1个从节点，接入系统应根据实际需求调整分片和从节点数量；
推荐用于需要大规模数据存储或高并发请求访问的场景，在该模式下支持横向、纵向扩展，Redis集群会识别各分片主节点健康状态，异常情况下会对故障分片进行主从切换；
主从切换时，接入系统客户端会自动识别Redis集群主节点地址并重新连接。
缓存服务支持开源Redis的数据结构和命令，同时支持根据业务特点选择持久化模式、数据淘汰策略，接入系统应根据业务需求明确相关服务端配置。
服务容灾
缓存服务提供跨机房的数据同步以及路由网关高阶能力，用于支撑接入系统双多活或单元化建设，接入系统应根据业务特点选择缓存高阶能力。
数据同步能力：缓存服务基于Redis原生PSYNC能力进行增强，实现Redis集群间数据同步，提供了级联同步、流量回环识别、逻辑时钟校验等功能。
路由网关能力：缓存服务基于开源Predixy进行增强，实现了Redis路由网关能力，并提供了逻辑主从识别、读写分离、自动切流等功能。
设计指引
接入缓存服务时，应在系统设计阶段重点设计缓存依赖、数据拆分、数据隔离、接口熔断、数据多级存储方案。
缓存依赖
缓存组件作为性能提升的辅助手段，接入系统应根据缓存服务的依赖程度、接口重要性，设计缓存接口熔断、数据多级存储能力，关键交易接口不宜强依赖缓存服务。
缓存接口熔断：当接入系统访问缓存数据失效或不可用时，熔断接口。
数据多级存储：数据存储至缓存和数据库，当访问缓存数据失效或缓存服务不可用时，降级访问数据库。
数据隔离
接入系统应在本系统范围内使用缓存服务，不宜多个系统混用缓存服务，推荐根据系统可用性等级、数据重要等级拆分缓存数据，可参考以下数据隔离规则。
根据数据安全等级拆分缓存数据，存储至多套缓存服务。
根据数据业务领域拆分缓存数据（如根据微服务领域拆分），存储至多套缓存服务。
根据数据可用性等级拆分缓存数据（如管理类数据与业务类数据分离），存储至多套缓存服务。
根据数据访问频率拆分缓存数据，实现冷热数据隔离，热点数据存储于缓存服务，冷数据使用其余数据存储软件保存。
部署模式
接入系统应在设计阶段明确缓存服务的部署架构及服务端资源，应根据性能及数据量、可用性、数据持久化等要求设计。
性能及数据量
接入系统应在选择部署模式时考量性能和数据量要求，可参考以下服务规格选型。
缓存服务主从模式，推荐用于TPS低于20000且存储数据量低于10G的场景，其中存储数据大小应满足（存储数据≤10G）：
低配版本：节点资源1C/4G，存储数据使用上限2G；
标准版本：节点资源2C/8G，存储数据使用上限4G；
高配版本：节点资源4C/20G，存储数据使用上限10G。
缓存服务集群模式，推荐用于TPS超过20000或存储数据量高于10G，单个分片可存储10G数据，其中集群分片数量应满足（分片数=2n+1，n≥1），单个分片内存大小应满足（存储数据≤10G）：
标准版本：节点资源4C/8G（3分片，分片数根据内存和TPS需求确定），单分片存储数据使用上限4G；
高配版本：节点资源4C/20G（3分片，分片数根据内存和TPS需求确定），单分片存储数据使用上限10G。
可用性
接入系统推荐在选择部署模式时考量可用性要求，可参考以下可用性分析选型。
缓存服务主从模式可用性分析：
高可用：数据多副本，服务端高可用；
数据复制：主从节点复制存在时延，仅支持最终一致；
故障切换：由服务端进行故障切换，客户端重连可恢复。主节点异常时，故障恢复时间在分钟级；主从节点同时异常时，自动触发节点重建，故障恢复时间在20分钟内。
缓存服务集群模式可用性分析：
高可用：数据多副本，数据分片存储，服务端高可用；
数据复制：主从节点复制存在时延，仅支持最终一致；
故障切换：由服务端进行故障切换，客户端需配置定时更新Redis服务拓扑。主节点异常时，故障恢复时间根据客户端定时更新Redis服务拓扑周期完成切换，最低为秒级。超过一半Redis分片主从节点同时异常时，自动触发节点重建，故障恢复时间在20分钟内。
数据持久化
接入系统应在选择部署模式时考量持久化要求，重要业务数据应明确数据丢失风险并设计数据丢失处置方案，推荐设计数据全量导入定时任务等方案，应对缓存数据丢失场景，可参考以下持久化分析选型。
Redis内存模式：
仅在内存中缓存业务数据，通过Redis服务高可用能力保障数据高可用，但缓存数据未持久化保存，极端情况下可能丢失；
该模式下，服务性能最佳、数据可靠性差、服务自愈能力最佳，支持底层服务器异常情况下的自动漂移，接入系统在缓存非重要数据且接口为非核心接口时可使用该模式。
Redis持久化存储：
在内存中缓存业务数据并定时持久化到存储盘；
该模式性能较好、数据可靠性较好、服务自愈能力依赖底层环境（仅支持手动漂移至健康物理机）。
Redis内存模式+数据库多级存储：
针对核心交易类接口，使用Redis缓存模式存储数据，异常情况下可自动漂移恢复的能力，数据丢失情况下可访问数据库重新加载数据；
该模式兼顾数据可靠性和服务自愈能力。
其他
除上述参考设计外，接入系统可参考其余非功能需求指标进行选型。
部署区域
接入系统应合理选择部署区域，可参考以下原则选择。
接入系统与缓存服务推荐部署至相同网络安全域，避免跨网络域访问。
灾备、双活架构系统，应使用相同架构、规格的缓存服务。
缓存服务访问地址不能发布至公网。
功能接口
接入系统应根据缓存相关接口需求，设计数据淘汰策略、数据预热等方案，可参考以下原则设计接口。
数据淘汰：缓存数据应显式设置合理的失效时间（TTL），避免超出缓存容量或大量数据过期导致雪崩；应明确服务端数据淘汰策略参数（maxmemory-policy）配置，如不使用默认值，应在申请时说明该需求。
热点数据：高频访问的缓存数据接口推荐设计数据预热、多级缓存等机制，应设计数据库加锁、布隆过滤器等方案避免缓存击穿。
通知机制：
在使用缓存实现异步通知等场景中，应避免使用循环访问查询的模式，推荐通过Pub/Sub命令实现相应的功能；
针对键值类操作，推荐使用keyspace-notification机制，当执行缓存操作时会发送事件通知至订阅客户端，如需开启该配置，应评估该调整产生的额外性能、网络开销，并在申请时说明该需求。
数据一致：使用多级存储缓存数据时，应设计缓存、数据库的数据读写策略、数据一致性更新、并发控制、重试机制、缓存失效策略等方案。
缓存数据结构
接入系统应选择合适的数据结构存储缓存数据，使用键值数据结构时，可参考以下数据结构规范选型。
业务Key不宜使用特殊字符（空格、换行符、双引号及其他转义字符）。
业务Key推荐通过系统编号、模块区分如J036X0:order:Key1。
不宜使用大Key，string对象，存储数据量建议控制在10KB以内，集合对象（hash、list、set、zset等）存储数据量建议控制在5000项以内，如存储数据量超过5000项应均匀拆分至多个集合。
推荐选择合适的数据压缩算法，优化内存空间占用，推荐使用JSON、XML、binary-data压缩数据后再存入Redis。
非Lua场景下不宜使用hashtag，避免出现流量倾斜。
容灾功能
设计方案
接入系统在建设单元化/双多活能力时，应结合系统架构设计选择使用缓存服务高阶能力，可参考以下设计，在实际落地中可组合使用。
缓存服务机房独立部署、数据不同步，接入系统缓存数据单元化改造。
缓存服务机房独立部署，数据不同步，接入系统缓存数据无单元化改造，通过数据库同步业务数据。
缓存服务同城机房双向同步，接入系统缓存数据无单元化改造、读写请求均访问主机房缓存服务，支持手动/自动容灾切换。
缓存服务同城机房双向同步，接入系统缓存数据无单元化改造、写请求访问主机房缓存服务、读请求访问就近机房缓存服务，支持手动/自动容灾切换。
功能选型
接入系统明确设计方案后，应根据当前缓存服务容灾功能，结合业务特性进行功能选型，应考虑以下功能选型。
数据同步：
无需同步：热点缓存类数据优先使用单元化设计，缓存数据不进行跨机房同步。
单向同步：主机房同步数据至同城容灾机房缓存服务，容灾切换后需通过运维处置反转同步关系。缓存服务支持机房级数据同步，支持数据同步最终一致性。
双向同步：主机房、同城容灾机房缓存服务数据双向同步，容灾切换无额外数据同步操作。缓存服务支持机房级数据双向同步，解决数据回环、逻辑时钟问题，不支持数据双写，支持数据同步最终一致性。
流量路由：
Proxy容灾切换：主机房、同城容灾机房部署Proxy组件承载本机房缓存流量，容灾切换时，通过Proxy隔离故障缓存服务，并将缓存请求路由至同城容灾机房缓存服务。
DNS容灾切换：DNS域名解析至主机房缓存服务，容灾切换时，DNS将域名解析至同城容灾机房缓存服务。
容灾切换：
手动容灾切换：通过手动操作执行容灾切换。使用Proxy容灾切换时支持标准化缓存服务流量切换，使用DNS容灾切换时支持标准化域名解析切换。
自动容灾切换：提前配置健康检查，当健康检查失败触发异常时，自动执行容灾切换。使用Proxy容灾切换需配置故障切换周期、故障缓存分片数，满足容灾切换条件时可自动执行Proxy流量切换，使用DNS容灾切换需配置缓存服务故障切换周期、四层网络健康检查，满足容灾切换条件时可自动执行域名切换。
读写策略：
主机房读写：主机房缓存服务承载所有请求，同城容灾机房热备，主机房、同城容灾机房的Proxy组件将流量路由至主机房缓存服务。
读写分离：主机房缓存服务承载所有写请求，同城容灾机房承载本机房读请求，主机房、同城容灾机房的Proxy组件将写流量路由至主机房缓存服务，读流量路由至就近机房缓存服务。
客户端：接入系统客户端自动重连缓存服务设计。
缓存服务上述功能不推荐在异地容灾架构中使用，推荐异地分别使用两套独立的缓存服务，异地灾备切换时，可通过缓存数据初始化等方案加载缓存数据。
功能限制
接入系统使用缓存服务容灾功能时，应明确缓存服务功能限制，具体限制如下。
容灾切换：容灾切换选择Proxy组件自动容灾切换功能时，缓存服务容灾切换控制器不能处理网络分区，当出现网络分区时主机房、同城容灾机房缓存服务降级为两套独立的缓存服务。
数据一致性：读写策略选择读写分离功能时，数据机房同步存在毫秒级时延，写入数据后可能存在数据读取不存在，接入系统应明确同步时延对应用的影响后选择此方案，并通过重试等机制规避该限制。
接口限制：选择使用缓存服务Proxy组件时，缓存命令存在一定限制，不能支持事务、keys命令。
开发指引
接入系统在编码阶段应规范化缓存服务使用，包括服务端、客户端版本以及相关配置，应遵循开发规范。
服务端版本要求
应符合附录A相关文件要求的缓存服务版本。
客户端版本要求
缓存服务支持Jedis、Lettuce、Redisson客户端，因开源软件持续保持更新，客户端具体版本选择应根据最新开源技术目录，当前客户端版本要求具体见表5。





表5  客户端版本说明
客户端配置
客户端配置参数
接入系统使用客户端连接缓存服务时，应使用连接池模式接入并合理配置客户端参数（需合理配置连接池大小并在使用后及时释放连接）。下述为相关参数的配置建议，接入系统应结合系统设计、测试实际情况配置参数，具体见表6。
表6  客户端配置参数说明
客户端配置需根据接入系统性能、并发、响应时间等要求配置，在通过测试、验证后方可上线。
连接数参数
接入系统使用不同模式的缓存服务，部分客户端相关参数有所差异，应根据下列说明调整参数，并进行测试验证，具体见表7。
表7  连接数参数说明

拓扑刷新参数
客户端应配置拓扑刷新配置，在缓存服务重启、扩容、主从切换、异常宕机时，正常重连缓存服务，。在缓存服务集群模式下，客户端连接缓存服务发送请求会先获取缓存分片拓扑地址，然后分别连接各分片主节点发送数据，客户端缓存的缓存分片拓扑IP地址为动态分配。
如使用Jedis客户端，无需额外配置。
如使用Lettuce客户端，应按照以下要求配置客户端：
Springboot版本应大于2.3.0；
客户端应配置拓扑刷新开关、拓扑刷新检查周期参数。
重连重试参数
接入系统在连接缓存服务时，推荐配置重连重试相关参数，规避网络丢包场景下的连接超时问题。
如使用Jedis客户端，应配置maxWaitMillis、testOnBorrow、testWhileIdle参数。
如使用Lettuce客户端，应配置连接池最大阻塞等待时间参数，不推荐直接使用spring-redis默认配置，推荐重写RedisConfig配置类，并在SocketOptions配置中增加keepalive和tcpUserTimeout参数，相关参数配置需调整代码。
Lettuce客户端引入netty-transport-native-epoll依赖
Lettuce客户端配置keepalive和tcpUserTimeout参数
命令使用说明
接入系统使用客户端连接缓存服务时，应避免Redis命令使用不当引起系统性能、可用性问题。
高危命令
接入系统不能使用高危命令，包括CONFIG、FLUSHALL、FLUSHDB等修改服务端的命令，上述命令可能导致服务配置变更、数据异常丢失，影响接入系统可用性。
批量命令
接入系统应合理使用批量命令，在批量获取数据场景时，应评估数据效率和数据量级，可参考以下批量命令使用要点：
推荐合理使用MGET、MSET命令或Pipline等批量命令，避免通过循环GET的方式获取数据。
使用批量命令进行批处理任务操作时，应评估、控制单次处理的数据量。
不宜使用集合对象整存整取命令、集合高时间复杂度命令，避免出现慢日志问题，命令包括HGETALL、SMEMBERS、LRANGE 0 -1、ZRANGE -inf +inf、LREM、ZUNION等。
全库匹配命令
接入系统不能使用全库匹配命令（Keys命令），在键值索引时不能使用全库匹配关键字（* 匹配全库数据），推荐使用Scan命令和前缀关键字匹配替代。
键空间事件
接入系统应合理使用键空间事件，在配置keyspace-notification参数、选择事件监听范围，根据实际情况选择相关参数配置，具体见表8。
表8  键空间事件参数说明
事务命令
缓存服务不能支持强一致性事务，仅提供乐观锁和批量操作的最终一致性能力，不宜使用缓存服务处理事务。接入系统如需使用缓存服务事务功能，需充分评估一致性影响、事务异常设计、事务回滚方案，可参考下列命令设计。
提供SETNX命令可仅在键不存在时将键值设置为制定字符串，可通过相关该命令设计锁。
提供WATCH命令监听一个或多个键值，可在执行事务时使用该命令监听键是否被修改，键值如被修改则放弃执行事务。
提供MULTI命令开启事务，在MULTI执行后相关命令都会被缓存起来，调用后续命令才会执行。
提供DISCARD命令取消事务，MULTI执行后相关命令不会执行。
提供EXEC命令提交事务，如果事务中包含的命令出现错误，会继续执行剩余的命令，而不会回滚成功执行的命令。
容错开发说明
在编码过程中，接入系统应根据系统等级、可用性要求、灾难恢复要求，确认接口对缓存服务的依赖程度，并在设计缓存相关接口调用时评估容错机制，提升系统稳定性。
健康检查
接入系统可根据对缓存服务依赖程度设计健康检查接口，并从应用测设计缓存服务的可观测指标和应用健康检查接口。
可根据接入系统对缓存服务的依赖程度，设计缓存检查接口（Ping、Set/Get定时检查），并加入应用健康检查接口。
可根据接入系统对缓存服务的依赖程度，新增应用客户端访问缓存健康指标，并增加应用告警。
可根据应用对缓存服务的依赖程度，设计健康探测、自动重启（仅在应用主流程业务强依赖缓存服务且无法改造时，可使用此方案）。
异常处置
核心交易接口应保证其可靠性、鲁棒性，极端情况下出现基础软硬件环境异常（网络异常、物理设备异常）引起的缓存服务主从切换、全量宕机、网络异常时，核心交易接口应保持持续可用，推荐参考以下原则开发核心接口。
服务熔断：合理配置超时时间，当访问缓存服务出现异常时，熔断缓存访问请求。
服务降级：合理设计服务降级，当访问缓存服务出现异常时，降级访问数据库，保障核心交易接口正常返回。
错误处理：合理捕获异常，根据错误类型打印关键日志。
请求重试：重要数据类操作时，合理设计业务侧请求重试逻辑，针对网络抖动等场景捕获特定异常错误并重试请求，重试接口应满足幂等性和重复执行要求。
容灾开发说明
接入系统应在系统层面设计容灾接口，引入缓存服务容灾功能时，应根据缓存服务Proxy组件、容灾切换方案，在接口层面评估兼容性、数据一致性、容灾切换。
兼容性
容灾功能选用缓存服务Proxy组件时，部分命令、键值对存在使用限制。
客户端应按照主从模式进行配置。
客户端应配置重连相关配置，确保容灾切换后可自动重连。
不能使用keys命令，应使用scan命令替代。
不能使用multi、exec、discard等事务命令。
数据一致性
缓存服务Proxy开启读写分离后，写请求路由至逻辑主机房，读请求路由至就近机房，仅支持最终一致性，数据存在同步时延。接入系统应评估是否接受同步时延，并推荐在读取接口中增加重试逻辑。
容灾切换
容灾功能选用缓存服务Proxy组件时，容灾切换支持主动切换和手动切换两种模式，接入系统应根据RTO、RPO选择容灾切换方案，确保切换方案的稳定性和可靠性。
主动切换：缓存服务控制器定时检测主机房缓存服务健康状态，出现异常后读写流量将切换至灾备机房缓存服务，接入系统需明确健康检查的周期、触发容灾切换的缓存分片数量。
手动切换：缓存服务控制器定时检测主机房缓存服务健康状态，出现异常后，需要运维人员介入手动将读写流量切换至灾备机房缓存服务。
安全编码
接入系统应结合系统安全设计，遵循相关的安全原则。
服务认证：应开启客户端认证，根据密码规范配置接入密码。
数据加密：业务数据应加密后存储至缓存服务，满足本行数据安全要求。
测试指引
接入系统在测试阶段，应规范化缓存服务相关接口测试过程，按照测试应进行功能及性能测试，推荐增加专项测试，以验证在某些故障场景下系统的应对能力，确保符合接入系统的功能要求和可用性要求。
性能测试
接入系统测试缓存相关接口性能时，推荐使用全链路性能测试，提前评估缓存容量、TPS、QPS、铺底数据，设计相关性能测试案例，确保接口符合性能要求。
专项测试
接入系统需要评估缓存服务的异常切换、宕机影响，推荐在专项测试中重点评估以下场景对接入系统的影响，明确接入系统在故障过程中、故障恢复后的业务影响，可参考以下专项测试案例。
表9  专项测试案例说明
可参考上述案例，根据接入系统可用性要求补充混沌案例进行专项测试。
上线指引
接入系统在上线阶段，应从系统维度准备生产下发方案并识别风险，结合技术中台相关服务接入指引和运维单位要求，完成上线前置准备、下发检查、告警规则调整和应急卡片编写等工作。
前置资源准备
接入系统在生产环境接入缓存服务，推荐通过IT综合管理系统发起软件维护需求，在施工完成后，将反馈回执信息至申请单位。
在申请软件维护需求时，应在流程附件中提供系统概要设计说明书并明确服务资源需求，应重点关注：接入区域、服务部署模式、资源需求、持久化模式和容灾要求，并根据本文设计指引确定是否存在定制化需求，如淘汰策略、配置参数等，也需在流程附件中说明。
告警规则确认
缓存服务默认接入技术中台可观测底座，提供标准化的监控、日志、告警能力。接入系统可根据业务本文设计指引，评估服务默认模板的监控项、告警阈值是否满足需求，并根据业务特点调整监控项和告警项，研发测试环境验证通过后提交至生产应用运维人员更新生产环境监控指标及告警规则。
接入前置检查
接入系统在上线或首次接入缓存服务时，应完成系统投产及维护下发前的检查核对工作，包括客户端配置确认、生产服务检查等，并根据缓存服务回执单，联系生产应用运维人员完成生产资源接入前检查，包括服务部署模式确认、生产资源确认、网络连通性确认、连接认证确认等，确保接入系统客户端配置信息准确无误。
应急卡片准备
接入系统在上线或首次接入缓存服务时，应结合缓存服务使用情况完成接入系统的应急预案（卡片）编写，并提交至生产应用运维人员。


（规范性）
指导文件
A.1  行内指导文件
本文件应符合行内指导文件要求，包括但不限于：
兴业银行，《兴业银行技术平台目录》；
兴业银行，《兴业银行软件技术平台版本序列及兼容列表》。
未注明发文号的，应遵照最新版本。
_________________________________


|  |
| --- |


| 模式 | 说明 |
| --- | --- |
| 单点模式 | 该模式无高可用能力，数据仅存在于一台Redis节点上 |
| 主从模式 | 该模式通过增加Redis从节点实现数据高可用，数据定时由Redis主节点同步至Redis从节点，当主节点发生异常时，需手动切换主从 |
| 哨兵模式 | 该模式在主从模式的基础上，增加了Redis哨兵节点。哨兵节点会定时检查Redis主节点是否存活，当Redis主节点发生异常时，切换Redis主从关系，实现Redis故障时自动切换 |
| 集群模式 | 该模式在Redis主从模式的基础上，增加了数据分片能力。缓存数据会被分片存储在多套Redis节点中，每套Redis通过主从模式实现数据高可用，当某个分片主节点发生异常时，Redis集群可自动识别节点状态，切换故障Redis分片的主从关系 |


| 模式 | 说明 |
| --- | --- |
| 内存模式（默认模式） | 该模式下Redis仅将数据存储至内存，无数据持久化，此模式性能最佳、数据可靠性差、发生故障时恢复较简单也较快 |
| RDB模式 | 该模式下Redis数据存储于内存，同时定时持久化全量数据至硬盘，该模式性能较好、数据可靠性较好、发生故障时因涉及持久化数据恢复恢复时间较长 |
| AOF模式 | 该模式下Redis数据存储于内存，同时每秒持久化增量数据至硬盘，该模式性能最差、数据可靠性最佳、发生故障时因涉及持久化数据恢复恢复时间较长 |


| 数据类型 | 说明 |
| --- | --- |
| 字符串（String） | 存储一个字符串值，也可存储文本、整数或二进制数据，常用于缓存、计数器、分布式锁等场景 |
| 哈希（Hash） | 存储键值对集合，每一个键都对应一个哈希表，常用于存储对象属性、配置等 |
| 列表（List） | 存储一个有序的字符串队列，支持头部和尾部的插入、删除及索引访问操作，常用于动态数据等场景 |
| 集合（Set） | 存储一组唯一的字符串集合，支持交集、并集、差集操作，常用于存储唯一标识、用户关联等场景 |
| 有序集合（SortedSet） | 在集合的基础上每个元素都关联一个分数，支持集合排序、根据分数范围获取元素的操作，常用于优先队列等场景 |
| 位图（Bitmap） | 存储位操作相关的数据，支持位设置、清除、统计等操作，常用于用户统计等场景 |


| 数据类型 | 说明 |
| --- | --- |
| Noeviction（默认配置） | 不进行数据淘汰清理，当内存占用达到上限时拒绝写入操作并返回客户端错误信息，此时只响应读操作 |
| volatile-lru | 达到内存占用上限时，使用LRU算法（Last Recently Used）对具有有效期属性（expired属性）的键值数据进行筛选剔除，未配置expired属性的键值数据不受影响 |
| allkeys-lru | 达到内存占用上限时，使用LRU算法（Last Recently Used）剔除所有键值数据 |
| volatile-ttl | 达到内存占用上限时，根据键值数据中Key值的TTL属性剔除即将过期的键值键值数据，未配置expired属性的键值数据不受影响 |
| volatile-random | 达到内存占用上限时，随机剔除过期的键值数据，未配置expired的键值不受影响 |
| allkeys-random | 达到内存占用上限时，随机剔除所有键值数据 |
| volatile-lfu | 达到内存占用上限时，使用LFU算法（Least Frequently Used）对具有有效期属性（expired属性）的键值数据进行筛选剔除，未配置expired属性的键值不受影响 |
| allkeys-lfu | 达到内存占用上限时，使用LFU算法（Least Frequently Used）剔除所有键值数据 |


| 客户端类型 | 版本要求 | 是否纳入开源技术目录 | 说明 |
| --- | --- | --- | --- |
| Jedis | ≥4.4.0
≥3.10 | 是 | 4.4.0、3.10.0版本对于DNS解析\服务断联功能进行优化 |
| Lettuce | ≥6.3.0 | 是 | 6.3.0版本增加tcpTimeout参数配置 |
| Redisson | / | 否 | 非开源技术目录软件，不推荐使用 |


| 客户端 | 连接配置 | 说明 | 默认参数 | 配置要求 |
| --- | --- | --- | --- | --- |
| Jedis | maxTotal | 客户端最大连接数 | 8 | 1.无特殊需求配置应小于200
2.根据接入系统并发度及性能测试结果确认配置 |
| Jedis | maxIdle | 最大空闲连接数 | 8 | 1.无特殊需求配置为maxTotal/2
2.根据接入系统并发度及性能测试结果确认配置 |
| Jedis | minIdle | 最小空闲连接数 | 0 | 1.并发度较低可配置为0
2.并发度较高可配置为maxIdle，启动时预热连接池
3.根据接入系统并发度及性能测试结果确认配置 |
| Jedis | maxWaitMillis | 连接池最大阻塞等待时间，默认在访问超时将无限等待 | -1（单位ms） | 1.禁止配置为默认值
2.常见配置区间在50ms至5s
3.根据接入系统并发度及性能测试结果确认配置 |
| Jedis | testOnBorrow | 使用连接池连接前检查连接可用性，配置后每次获取连接将执行一次ping，开启后可确保连接可用性，会造成性能损耗 | false | 1.建议配置为true
2.根据响应时间需求及性能测试结果确认配置 |
| Jedis | testOnReturn | 归还连接池连接前检查连接可用性，配置后每次归还连接将执行一次ping，开启后可确保连接可用性，会造成性能损耗 | false | 1.建议配置为true
2.testOnBorrow配置为true时，可使用默认值
3.根据响应时间需求及性能测试结果确认配置 |
| Jedis | timeout | Redis请求访问的timeout | 2000（单位ms） | 1.无特殊需求使用默认值
2.根据响应时间需求及性能测试结果确认配置 |
| Jedis | connection-timeout | 创建连接时timeout | 2000（单位ms） | 1.无特殊需求使用默认值
2.根据响应时间需求及性能测试结果确认配置 |
| Jedis | blockWhenExhausted | 连接池用尽后是否等待，开启后根据maxWaitMillis参数确定 | true | 无特殊需求使用默认值 |
| Jedis | testWhileIdle | 空闲连接池检查，根据实际业务需求配置 | false | 无特殊需求时配置为true |
| Jedis | timeBetweenEvictionRunsMillis | 空闲连接检查周期，默认不检查 | -1（单位ms） | 1.禁止配置为默认值
2.常见配置区间在20s至300s
3.根据性能测试结果确认配置 |
| Lettuce | lettuce.pool.max-active | 客户端最大连接数 | 8 | 1.无特殊需求配置应小于200
2.根据接入系统并发度及性能测试结果确认配置 |
| Lettuce | lettuce.pool.max-idle | 最大空闲连接数 | 8 | 1.无特殊需求配置为max-active/2 
2.根据接入系统并发度及性能测试结果确认配置 |
| Lettuce | lettuce.pool.min-idle | 最小空闲连接数 | 0 | 1.并发度较低可配置为0
2.并发度较高可配置为max-idle，启动时预热连接池
3.根据接入系统并发度及性能测试结果确认配置 |
| Lettuce | lettuce.pool.max-wait | 连接池最大阻塞等待时间 | -1（单位ms） | 1.禁止配置为默认值
2.常见配置区间在50ms至5s
3.根据接入系统并发度及性能测试结果确认配置 |
| Lettuce | timeout | Redis请求访问的timeout | 2000（单位ms） | 1.无特殊需求使用默认值
2.根据响应时间需求及性能测试结果确认配置 |
| Lettuce | connection-timeout | 创建连接时timeout | 2000（单位ms） | 1.无特殊需求使用默认值
2.根据响应时间需求及性能测试结果确认配置 |
| Lettuce | lettuce.cluster.refresh.adaptive | 拓扑刷新开关，开启后可周期性获取Redis节点IP并更新客户端拓扑 | false | 禁止配置为默认值 |
| Lettuce | lettuce.cluster.refresh.period | 拓扑刷新检查周期，配置时间为获取Redis节点IP并更新客户端拓扑的周期 | 30s | 1.无特殊需求使用默认值
2.根据接入系统性能测试结果调整 |


| 客户端 | 配置参数 | 服务模式 | 配置说明 |
| --- | --- | --- | --- |
| Jedis | maxTotal、maxIdel | Redis主从模式 | 客户端连接均连接至缓存主节点，缓存服务总连接数 = 配置连接数 * 客户端副本数 |
| Jedis | maxTotal、maxIdel | Redis集群模式 | 客户端连接分别连接缓存各分片主节点，缓存服务总连接数 = （ 配置连接数 * 分片数 ） * 客户端副本数 |
| Jedis | maxTotal、maxIdel | Redis容灾模式 | 客户端均连接到Proxy组件，缓存服务总连接数 = 配置连接数 * 客户端副本数 |
| Jedis | minIdel | Redis主从模式 | 无特殊要求 |
| Jedis | minIdel | Redis集群模式 | 无特殊要求 |
| Jedis | minIdel | Redis容灾模式 | 客户端连接Proxy均匀分布，需配置连接预热，minIdel与maxIdel配置为相同大小 |
| Lettuce | lettuce.pool.max-active、lettuce.pool.max-idle | Redis主从模式 | 客户端连接均连接至缓存主节点，缓存服务总连接数 = 配置连接数 * 客户端副本数 |
| Lettuce | lettuce.pool.max-active、lettuce.pool.max-idle | Redis集群模式 | 客户端获取拓扑地址后，均连接至缓存分片的主节点，缓存服务总连接数 = （ 配置连接数*分片数 ） * 客户端副本数 |
| Lettuce | lettuce.pool.max-active、lettuce.pool.max-idle | Redis容灾模式 | 客户端均连接到Proxy组件，缓存服务总连接数 = 配置连接数 * 客户端副本数 |
| Lettuce | lettuce.pool.min-idle | Redis主从模式 | 无特殊要求 |
| Lettuce | lettuce.pool.min-idle | Redis集群模式 | 无特殊要求 |
| Lettuce | lettuce.pool.min-idle | Redis容灾模式 | 客户端连接Proxy均匀分布，需配置连接预热，min-idle与max-idle配置为相同大小 |


| <!-- maven依赖中引入netty-transport-native-epoll，此处仅供示例参考 -->
 <!-- 根据应用系统架构动态编译，通过命令指定-Px86 或 -Parm64 -->
  <profiles>
    <profile>
      <id>x86</id>
      <activation>
        <os>
          <arch>arm64</arch>
        </os>
      </activation>
      <dependencies>
        <dependency>
          <groupId>io.netty</groupId>
          <artifactId>netty-transport-native-epoll</artifactId>
          <!-- 需根据实际情况调整，netty使用4.x Release版本-->
          <version>xxx</version>
          <classifier>linux-x86_64</classifier>
        </dependency>
      </dependencies>
    </profile>
    <profile>
      <id>arm64</id>
      <activation>
        <os>
          <arch>arm64</arch>
        </os>
      </activation>
      <dependencies>
        <dependency>
          <groupId>io.netty</groupId>
          <artifactId>netty-transport-native-epoll</artifactId>
          <artifactId>netty-transport-native-epoll</artifactId>
          <!-- 需根据实际情况调整，netty使用4.x Release版本-->
          <version>xxx</version>
          <classifier>linux-arm64</classifier>
        </dependency>
      </dependencies>
    </profile>
  </profiles> |
| --- |


| // 此处仅供示例参考，根据应用代码调整配置，并在测试验证后使用
@Configuration
@EnableCaching
@ConfigurationProperties(prefix = "spring.redis")
public class RedisConfig extends CachingConfigurerSupport {
     /**
     *  TCP_KEEPALIVE打开，并且配置三个参数分别为本行标准值，参考《RedHat 7操作系统安装配置标准作业程序》（兴银TZ202403395）通知：
     *  TCP_KEEPIDLE = 150
     *  TCP_KEEPINTVL = 5
     *  TCP_KEEPCNT = 6
     */
    private static final int TCP_KEEPALIVE_IDLE = 150;
private static final int TCP_KEEPALIVE_INTVL = 5;
private static final int TCP_KEEPALIVE_CNT = 6;
    /**
     * TCP_USER_TIMEOUT参数可避免在故障宕机场景下，Lettuce持续超时的问题。
     * refer: https://github.com/lettuce-io/lettuce-core/issues/2082
     * TCP_USER_TIMEOUT = TCP_KEEPIDLE + TCP_KEEPINTVL*TCP_KEEPCNT
     * 对于网络异常的容忍度较低可配置TCP_USER_TIMEOUT = 30 （避免配置过小会无法容忍网络抖动）
     */
    private static final int TCP_USER_TIMEOUT = 180;
    //【重要】application.yaml中配置的参数注入需要全部注入到LettucePoolingClientConfiguration中
    @Value("${spring.redis.cluster.nodes}")
    private String clusterNodes;
    @Value("${spring.redis.cluster.max-redirects}")
    private String[] clusterMaxRedirects;
    // Redis服务器连接密码（默认为空）
    @Value("${spring.redis.password}")
    private String password;
    // 连接超时时间（毫秒）
    @Value("${spring.redis.timeout}")
    private Integer timeout;
    // 连接池最大连接数（使用负值表示没有限制）
    @Value("${spring.redis.lettuce.pool.max-active}")
    private Integer maxTotal;
    // 连接池最大阻塞等待时间（使用负值表示没有限制）
    @Value("${spring.redis.lettuce.pool.max-wait}")
    private Integer maxWait;
    // 连接池中的最大空闲连接
    @Value("${spring.redis.lettuce.pool.max-idle}")
    private Integer maxIdle;
    // 连接池中的最小空闲连接
    @Value("${spring.redis.lettuce.pool.min-idle}")
    private Integer minIdle;

     /**
     * 获取缓存操作助手对象
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate() {
        // 【重要】自定义RedisTemplate，通过getConnectionFactory获取连接工厂创建，此处仅为示例，需调整此处代码
        RedisTemplate<String, Object> template = new RedisTemplate<String, Object>();
        template.setConnectionFactory(getConnectionFactory());
        StringRedisSerializer stringRedisSerializer = new StringRedisSerializer();
        //RedisTemplate对象需要指明Key序列化方式，如果声明StringRedisTemplate对象则不需要
        template.setKeySerializer(stringRedisSerializer);
        // hash的key也采用String的序列化方式
        template.setHashKeySerializer(stringRedisSerializer);
        // value序列化方式采用String
        template.setValueSerializer(stringRedisSerializer);
        template.afterPropertiesSet();
        return template
    }

    /**
     * 获取缓存工厂对象
     */
    @Bean
    public RedisConnectionFactory getConnectionFactory() {
           // 【重要】自定义RedisConnectionFactory 通过getPoolConfig获取连接池配置创建，此处仅为示例，需调整此处代码
            RedisClusterConfiguration configuration = new RedisClusterConfiguration();
            String[] nodes = clusterNodes.split(",");
            for (String node : nodes) {
                String[] redisInfo = node.split(":");
                configuration.clusterNode(redisInfo[0], Integer.parseInt(redisInfo[1]));
            }
            configuration.setPassword(RedisPassword.of(password));
            LettuceConnectionFactory factory = new LettuceConnectionFactory(configuration, getPoolConfig());
            return factory;
    }
    /**
     * 获取缓存连接池配置对象
     */
    @Bean
    public LettucePoolingClientConfiguration getPoolConfig() {
        GenericObjectPoolConfig config = new GenericObjectPoolConfig();
        config.setMaxTotal(maxTotal);
        config.setMaxWaitMillis(maxWait);
        config.setMaxIdle(maxIdle);
        config.setMinIdle(minIdle);
        ClusterTopologyRefreshOptions topologyRefreshOptions = ClusterTopologyRefreshOptions.builder().enablePeriodicRefresh(refreshAdaptive).refreshPeriod(Duration.ofMillis(refreshPeriod)).build();
        //【重要】关键配置修改，keepalive和tcpUserTimeout配置
        SocketOptions socketOptions = SocketOptions.builder().keepAlive(SocketOptions.KeepAliveOptions.builder().enable().idle(Duration.ofSeconds(TCP_KEEPALIVE_IDLE)).interval(Duration.ofSeconds(TCP_KEEPALIVE_INTVL)).count(TCP_KEEPALIVE_CNT).build()).tcpUserTimeout(SocketOptions.TcpUserTimeoutOptions.builder().enable().tcpUserTimeout(Duration.ofSeconds(TCP_USER_TIMEOUT)).build()).build();
        //下列配置为集群模式例子，主从模式可使用ClientOptions
        ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder().topologyRefreshOptions(topologyRefreshOptions).socketOptions(socketOptions).build();

        LettucePoolingClientConfiguration pool = LettucePoolingClientConfiguration.builder().clientOptions(clusterClientOptions).poolConfig(config).commandTimeout(Duration.ofMillis(timeout)).build();
        return pool;
    }
} |
| --- |


| 参数配置 | 配置范围 | 说明 |
| --- | --- | --- |
| K | 监听Keyspace事件开关 | 配置后可通过SUBSCRIBE命令订阅键值的变化，订阅事件为__keyspace@<db>__<键值>，返回结果为执行的指令 |
| E | 监听Keyevent事件开关 | 配置后可通过SUBSCRIBE命令订阅Redis指令，订阅事件为__keyevent@<db>__<指令>，返回结果为键值 |
| g | 监听事件范围配置 | 监听非特定的通用命令，DEL、EXPIRE、RENAME等命令 |
| $ | 监听事件范围配置 | 监听字符串（String）命令 |
| l | 监听事件范围配置 | 监听列表（List）命令 |
| s | 监听事件范围配置 | 监听集合（Set）命令 |
| h | 监听事件范围配置 | 监听哈希（Hash）命令 |
| z | 监听事件范围配置 | 监听有序集合（SortSet）命令 |
| t | 监听事件范围配置 | 监听流命令 |
| x | 监听事件范围配置 | 监听过期命令 |
| e | 监听事件范围配置 | 监听淘汰命令 |
| m | 监听事件范围配置 | 监听未命中命令 |
| A | 监听事件范围配置 | 监听上述所有命令 |


| 专项测试案例 | 测试说明 |
| --- | --- |
| 缓存服务（应用端）网络抖动演练 | 本场景模拟应用网络抖动场景出现应用到Redis（主从模式/集群模式）间数据包丢包（可配置丢包率及丢包时间），验证应用层是否具备重试写入机制。 |
| 缓存服务极端场景全量宕机演练 | 本场景模拟Redis服务（主从模式/集群模式）因故障全部宕机，验证应用故障处置后自动重连能力 |
| 缓存服务（主从模式）主从切换演练 | 本场景模拟Redis（主从模式）发生主从切换场景，验证应用自动重连能力 |
| 缓存服务（集群模式）分片故障演练 | 本场景模拟Redis（集群模式）发生分片全部故障场景下，验证应用自动重连能力 |
| 缓存服务（集群模式）分片主从切换演练 | 本场景模拟Redis（集群模式）发生分片主从切换场景下，验证应用是否可完成自动重连 |
| 缓存服务（容灾模式）容灾切换演练 | 本场景模拟Redis在同城双活部署架构（技术中台高阶能力）下，当一地Redis服务出现全部宕机时，应用是否可自动切换至另一地Redis服务 |
