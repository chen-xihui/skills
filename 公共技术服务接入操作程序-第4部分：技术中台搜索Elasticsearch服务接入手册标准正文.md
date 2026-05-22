Q/CIB
兴业银行股份有限公司企业标准
Q/CIB 4052.4—2025


公共技术服务接入操作程序 第4部分：
技术中台Elasticsearch服务接入手册
Public technical service access operation procedures—Part 4:
technical central platform Elasticsearch service access handbook

2025-11-30发布
2025-11-30实施
兴业银行股份有限公司发布
ICS 35.240.40
CCS A 11


目  次
目  次	I
前  言	III
公共技术服务接入操作程序 第4部分：技术中台Elasticsearch服务接入手册	1
1 范围	1
2 规范性引用文件	1
3 术语和定义	1
4 缩略语	3
5 基本概念	3
5.1 部署模式	3
5.2 持久化模式	4
6 服务介绍	4
6.1 服务特点	4
6.2 服务模式	4
7 设计指引	5
7.1 Elasticsearch依赖	5
7.2 数据隔离	5
7.3 部署模式	5
7.4 部署区域	7
7.5 功能设计	7
8 开发指引	12
8.1 服务端版本指引	12
8.2 客户端版本指引	13
8.3 安全编码	13
8.4 配置说明	13
8.5 应用开发说明	14
8.6 容错开发说明	26
9 测试指引	28
9.1 性能测试	28
9.2 专项测试	28
10 上线指引	29
10.1 前置资源准备	29
10.2 告警原则确认	29
10.3 接入前置检查	29
10.4 应急卡片准备	29
附　录　A  （规范性） 指导文件	30
A.1  行内指导文件	30
a) 兴业银行，《兴业银行技术平台目录》。	30
b) 兴业银行，《兴业银行软件技术平台版本序列及兼容列表》。	30

前  言
本文件按照GB/T 1.1—2020《标准化工作导则 第1部分：标准化文件的结构和起草原则》给出的原则起草。
本文件由总行科技管理部提出并归口。
本文件起草单位：总行科技管理部技术服务中心。
本文件主要起草人：吴清涛、林鑫。
本文件为首次发布。
公共技术服务接入操作程序
第4部分：技术中台Elasticsearch服务接入手册
范围
本文件给出了接入系统使用Elasticsearch服务时应遵循的设计原则、编码规范、测试要求，引导接入系统合理、高效地使用公共技术服务，提升应用的稳定性与可维护性。
本文件适用于境内外各分行、总行各部门、各子公司具有研发、运维职能的单位。
规范性引用文件
本文件没有规范性引用文件。
术语和定义

技术中台  technical middle platform
将本行公共的、通用的关键基础技术资源集中建设和维护，以平台形式提供技术服务。
技术中台包括应用开发平台、Devops与研发保障、应用集成、微服务支撑与治理、数字化运营与支撑、通用技术服务、基础PaaS、容器云平台八大板块。

技术中台Elasticsearch服务  technical middle office Elasticsearch Service;ES
Elasticsearch服务
技术中台基于云原生Operator技术，将Elasticsearch软件实现PaaS化，并作为一类基础技术服务进行提供，具备按需申请、快速交付、局部故障自愈和高可用性等特性。
根据JR/T 0166—2020定义，PaaS（platform as a Service，平台即服务）为云服务类别中的一种。
Operator是一种用于管理Kubernetes集群中复杂应用的工具，基于Kubernetes的控制器，自动化复杂应用的部署、管理和运维过程。

Elasticsearch
Elasticsearch是一个基于Apache Lucene的分布式、高扩展、高实时的全文搜索与数据分析引擎，支持快速高效存储和索引数据。
来源自Elasticsearch官方网站，https://elastic.co。

集群  cluster
cluster为Elasticsearch的最小服务实体，集群包含多个节点，主节点负责管理集群范围内的所有变更，例如增加、删除索引，或者增加、删除节点等。

节点  node
集群中的一个应用实例节点，运行态为Java进程，可通过增加或者减少节点实现集群扩容或缩容。

索引  index
索引为文档的集合，数据存储在单个或者多个Index中，单个索引有一个或者多个分片，索引支持将数据分散到多个分片中存储，实现高可用。

分片  shards
分片为数据存储的容器，单个完整索引可分成多个分片，分布到不同节点，构成分布式集群；当集群规模扩大或者缩小时，Elasticsearch会自动的在各节点中迁移分片，使得数据仍然均匀分布在集群里。

主分片  primary shards
索引存在主分片，在创建索引时确定主分片数。

副本分片  replica shards
每个索引支持多个副本分片，通过副本分片可以提高系统的容错性，当某个主分片损坏或丢失时可以从副本中恢复，同时提高查询效率，自动对索引请求进行负载均衡。

文档  doc
文档为索引内的数据内容，支持数据检索，通过对文档进行索引、检索、排序和过滤，实现搜索能力。

字段  field
字段为文档的子集数据，每个字段具备不同的类型，常见类型包括keyword、text、数字（integer、long、float、double）、对象等。

词项  term
词项为全文本的内容在分词后得到的词语，例如对“中国人”使用标准分词器分词后得到[中国人，中国，人]这3个词项。

聚合查询  aggregations
聚合查询（Aggregations）用于对数据进行统计、分析和分组，可以帮助用户从数据中提取有价值的信息，如统计某个字段的分布、计算总和、平均值等。请根据具体需求选择合适的聚合类型，并结合性能优化策略，确保查询高效准确。
缩略语
下列缩略语适用于本文件。
TPS：每秒事务处理数（Transactions Per Second）
VIP：虚拟IP地址（Virtual IP）
JSON：JS对象简谱（JavaScript Object Notation）
XML：可扩展标记语言（eXtensible Markup Language）
DNS：域名系统（Domain Name System）
基本概念
部署模式
Elasticsearch服务提供角色分离模式、混合模式两种不同的部署模式，接入系统可根据可用性要求和数据量选择，具体可见表1。
表1  部署模式分类
表2  常用节点角色
持久化模式
ElasticSearch服务默认开启持久化能力，所有数据均存储于本地存储盘，但数据落盘过程非强一致，无法确保RPO=0，具体说明如下。
索引数据写入内存缓冲区，内存缓冲区占满或固定时间间隔（默认值1s）使用refresh操作将内存缓冲区中数据生成index segment文件，并写入Translog日志文件系统缓存区，此时index segment可提供search查询读取；
内存缓冲区写入文件系统缓冲区后会清空，继续写入数据；
Translog日志文件达到阈值或固定时间间隔（默认值30s）会触发flush操作，文件系统中缓存的index segment文件被fsync强制写入磁盘，并清理Translog。
表3  Translog刷盘方式分类
服务介绍
服务特点
Elasticsearch服务提供了高效管理Elasticsearch实例生命周期的能力，可快速部署、配置、管理Elasticsearch服务实例，接入系统无需关注底层部署服务器资源及技术细节，应重点关注如何正确、合理地使用Elasticsearch能力，当前Elasticsearch服务具备以下特性。
多部署模式支持：支持混合部署和角色分离部署，满足不同业务场景需求。
信创适配：支持鲲鹏、海光芯片、麒麟操作系统，具备全栈信创支持能力。
局部故障自愈：可在服务器宕机等异常场景时，自动恢复、重启Elasticsearch服务，尽量减少故障影响。
高可用性：索引多分片以及有副本分片备份的情况下，当网络异常、服务器异常导致部分Elasticsearch节点异常主分片失效时，Elasticsearch可以提升副本分片为主分片，继续提供读写服务。
服务模式
Elasticsearch服务当前提供两种部署模式：混合模式、角色分离模式，均支持数据备份和故障场景下高可用，接入系统应根据两类模式特点，结合业务需求进行选择。
Elasticsearch服务混合部署模式：
集群内各节点角色相同，任何一个节点均可以成为master节点，每个节点也都存储数据，一般设置3个及以上奇数个节点。
该模式扩展灵活性相对较差，推荐用于小规模，无扩展需求的应用。
Elasticsearch服务角色分离部署模式：
集群内提供多种角色的节点，包括master节点（3个），data节点（根据业务数据量确定）以及client节点。
扩展灵活性高，可扩展特定类型节点数量，推荐用于需要大规模数据存储或高并发请求访问的场景。
设计指引
接入Elasticsearch服务时，应在系统设计阶段重点设计Index mapping、index主分片、index副本分片、分词器选择等方案。
Elasticsearch依赖
Elasticsearch组件可提升数据查询效率，推荐用于交易系统之外需要高效搜索和实时数据分析的场景中，接入系统应根据Elasticsearch服务的依赖程度、接口重要性，设计Elasticsearch接口熔断、数据多级存储能力，关键交易接口不应强依赖Elasticsearch服务。
交易类接口：接入系统在设计交易接口时不应强依赖Elasticsearch服务，当访问索引数据失效或不可用时，应降级处理请求，确保交易不受影响。
非交易类接口：接入系统在设计非交易接口时，应充分评估接口影响范围，避免搜索接口异常造成主体业务不可用，同时应考虑接口熔断设计，提升系统鲁棒性。
数据隔离
接入系统应在本系统范围内使用Elasticsearch服务，不宜多个系统混用Elasticsearch服务，推荐根据系统可用性等级、数据重要等级拆分索引数据，可参考以下数据隔离原则。
根据数据业务领域拆分索引数据，存储至多套Elasticsearch服务，如无特殊需求同一领域各微服务可使用一套Elasticsearch服务存储数据，推荐使用索引进行业务逻辑隔离。
根据业务可用性等级拆分索引数据：关键核心业务推荐使用独立Elasticsearch服务强隔离数据；默认场景下采用索引进行业务逻辑隔离。
部署模式
接入系统应在设计阶段明确Elasticsearch服务的部署架构及服务端资源，应根据性能及数据量、可用性、数据持久化等要求设计。
性能及数据量
根据复杂度和功能，查询可以分为简单查询和复杂查询；简单查询通常只包含单个字段或简单的条件匹配；复杂查询通常涉及多个条件、逻辑组合或高级功能。接入系统应在选择部署模式时根据业务考量性能和索引数据量要求，可参考以下服务规格选型：
低配版本：混合部署模式，节点资源2C/4G/100G,3分片，可支持复杂查询TPS≤500，简单查询TPS≤2000。
中配版本：分离部署模式，节点资源4C/8G/200G,3分片，可支持复杂查询TPS≤1000，简单查询TPS≤4000。
高配版本：分离部署模式，节点资源8C/16G/500G,3分片，可支持复杂查询TPS≤2000，简单查询TPS≤8000。
超高配版本：分离部署模式，节点资源16C/32G/1000G,分片N根据数据量确认，可支持复杂查询TPS≤1000*N，简单查询TPS≤4000*N。
磁盘容量规划可根据数据保存时间及大小进行估算，以实际需求进行扩容，建议根据以下计算方案进行估算存储使用量，单个节点存储上限为1000G：
日增量=文档数*单文档平均大小*副本数/压缩比（默认压缩算法LZ4）。
申请存储量=存储天数*日增量/70%(预留30%存储)。
上述TPS数据为实验环境测试结果，可能存在偏差，实际以测试结果为准。
持久化
接入系统应根据业务类型选择索引持久化的设计：
同步刷盘（默认配置）：订单、交易类等实时业务场景推荐使用，可确保数据可靠性，准实时可见。
异步刷盘：埋点类非实时业务场景推荐使用，可提升写入吞吐量，降低磁盘压力。
接入系统可根据业务类型在创建索引时配置，同时还应根据刷盘策略调整索引可见性配置，提升索引查看时效性：
配置索引同步刷盘
配置索引异步刷盘
其他
除上述参考设计外，接入系统可参考其余非功能需求指标进行选型。
部署区域
接入系统应合理选择部署区域，可参考以下原则选择：
接入系统与Elasticsearch服务推荐部署至相同网络安全域，避免跨网络域访问。
Elasticsearch服务访问地址不能发布至公网。
功能设计
接入系统应根据业务需求选择合适的分词器，创建索引，并使用Mapping、Analyzer、Filter构建索引的数据结构定义、文本处理流程、分词后处理。
命名设计
接入系统在创建索引、映射时应保持一致命名风格，避免使用特殊字符，推荐使用以下原则进行设计。
索引命名规范：以字母开头，长度在1～63个字符间，由小写字母、数字和下划线组成的字符串，索引命名应要清晰表达业务含义，如存在多语言场景使用，应增加语言标识后缀；如用户特征可命名为user_feature。
映射字段命名规范：以字母开头，长度在1～63个字符间，由小写字母、数字和下划线组成的字符串，字段命名应要清晰表达业务含义，如存在多语言场景使用，应增加语言标识后缀；如用户中文可命名为user_name_zh。
分词器选择
分词器（Analyzer）是Elasticsearch中用于将文本分割成单独的词条（token）的核心组件。分词器决定了文本如何被索引和查询，是Elasticsearch高效检索的基础。接入系统应根据语言、字段用途、搜索召回、性能等方面选择合适的分词器插件，目前提供的分词器及使用说明如下：
表4  分词器说明
索引设计
接入系统应在索引设计时考虑高可用方案、分片大小及分片分配策略，主要包括以下原则：
主分片数量：创建索引时必须指定主分片数量，且索引一旦创建主分片数将无法修改；推荐主分片数为数据节点的3倍，并确保单个索引分片存储不超过50GB，若数据量更大建议按时间或业务维度拆分索引。
分片副本数：创建索引时必须指定分片副本数，副本数最小设置为1，分片副本数越多，数据冗余越多，但会降低写入性能，普通系统推荐副本数设置为1，重要系统推荐副本设置为2。
分片数量限制：单个节点最大分片限制默认为1000，超过限制则无法创建新索引。
推荐使用索引模板规范索引配置。
Mapping设计
接入系统应通过Mapping设计定义索引中的字段和类型，通过Mapping定义选择不同字段的数据结构定义和分析器处理，可参考以下表格选择字段类型：
表5  字段说明

选择索引映射字段后，设计过程中应参考以下原则：
明确字段类型，合理设计字段，控制字段数量够用即可：
字段应显示定义，不推荐使用动态mapping，容易造成性能影响。
预留字段支持未来业务扩展，提升可扩展性。
中文字段、多语言推荐使用多字段配置：
同一字段推荐定义多个fields适配不同场景。
查询类型选择时，前缀通配符应与analyzer与token一致。
字段应按需配置分词检索：
没有检索需求的字段应在mapping中设置“index”为no，不设置分词和全文检索。
控制字段长度，避免大文本字段占用过多内存。
字段应按需配置聚合：
没有聚合需求的字段建议“doc_values”为false。
避免对大文本字段进行聚合，导致内存大量占用。
查询设计
接入系统应根据业务特定的用途和适用场景，选择合适的查询方式，以优化搜索性能和提升用户体验，以下是常见查询方式的对比总结：
表6  查询总结
接入系统在使用查询功能设计搜索能力时，应遵循一定的查询设计规范和原则，重点关注查询设计、性能优化、可维护性等部分：
功能选择上推荐参考以下原则：
查询选择DSL语法，不直接拼接字符串，避免注入。
多字段查询使用multi_match，单字段查询使用match。
精确匹配使用term/terms，模糊、全文匹配使用multi_match/match,避免混用。
复杂查询必须用bool，保持must、should、must_not、filter语义清晰。
排序字段必须使用keyword、numeric、date，禁止使用text。
性能优化时推荐参考以下原则：
推荐使用filter代替query，filter可以被缓存效率更高，适用于状态字段（status=active）、时间范围过滤。
避免高开销查询，减少wildcard、regexp适用，适用于前缀限制。
控制查询分页大小，避免深分页适用from+size，推荐使用search_after或scroll。
控制结果返回字段，避免使用全量_source。
聚合查询设计时推荐参考以下原则：
聚合字段必须使用keyword/numeric/date，不能对text聚合。
复杂多层聚合必须设置合理size大小，避免单次返回。
避免对高基数，大数量字段做terms聚合。
聚合结果排序时注意精度，必要时增加shard_size，share_size值可以基于分片数量计算，shard_size = 期望结果数 * 索引主分片数，比如有 5 个分片，期望返回 10 个结果，可以将 shard_size 设置为 10 * 5 = 50，具体值请根据业务量和响应时间对比验证后确认。
多字段设计时推荐参考以下原则：
对text字段使用多字段映射，通过multi-fields指定不同的类型和分词器用于不同的用途。
查询时根据需求选择合适的子字段，避免所有查询都在text上。
查询相关性设计与查询优化时推荐参考以下原则：
推荐使用字段权重使用^n或boost设置权重，例如title^3、content^1。
推荐使用function_score结合时间、权重调整评分。
推荐使用_explain API 优化搜索打分，排查索引设计不合理。
_explainAPI分析相关性
_profile 优化查询执行
开发指引
接入系统在编码阶段应规范化使用Elasticsearch服务，包括服务端、客户端版本以及相关配置，应遵循开发规范。
服务端版本指引
应符合我行开源技术目录的Elasticsearch服务端版本使用。
表7  服务端版本说明
客户端版本指引
推荐使用Elastic Java API Client客户端，客户端版本需选择和服务端版本一致：
表8  客户端版本说明
安全编码
接入系统应结合系统安全设计，遵循相关的安全原则，强制要求开启客户端认证，根据密码规范配置接入密码，禁止使用无认证的ElasticSearch服务。
配置说明
服务端配置参数
推荐接入系统使用默认服务端配置，Elasticsearch服务默认提供标准化配置，在性能优化、功能配置部分已可以满足需求，关键配置参数可参考下表：
表9  服务端关键配置参数
客户端配置参数
接入系统使用客户端连接索引服务时，应使用合理配置客户端参数并结合系统设计、测试实际情况配置参数，参数说明如下：
表10  客户端关键配置参数
应用开发说明
接入系统接入Elasticsearch服务时，需创建索引、文档，并对创建的文档进行查询和搜索。
索引初始化
接入系统接入Elasticsearch服务需通过REST API根据索引设计创建索引，并根据业务、文档类型设计配置mapping、分词器。针对类似规则的索引，可以定义索引模板用来简化后续的索引创建复杂度。如需修改索引模板，可以使用PUT请求重新定义模板。
修改模板不会影响已经存在的索引，只会对新创建的索引生效。
创建索引
创建或修改索引模板
JAVA客户端使用
接入系统接入Elasticsearch服务推荐使用co.elastic.client:elasticsearch-java客户端（下文简称为Es-JAVA客户端），接入系统如使用springboot框架，需注意以下问题：
Springboot3.x版本对应Spring Data Elasticsearch 5.x版本支持Elasticsearch 8.x版本。
Springboot2.x版本对应Spring Data Elasticsearch 4.x版本支持Elasticsearch 7.x版本。
初始化Es-JAVA客户端
初始化Springboot-data客户端
常用的客户端操作包括对索引的创建、删除、查询，在初始化客户端后可以参考以下示例：
索引相关操作
Elasticsearch服务的交互逻辑为文档的创建、删除和搜索，客户端提供全量搜索、分组搜索、模糊搜索、组合搜索、聚合搜索、范围搜索、条件搜索、分页搜索多种能力，可组合使用相关搜索实现业务的快速查询功能：
文档相关操作
接入系统还可以创建JAVA实体类，抽象Respository接口调用ElasticSearch服务，通过@Query注解定义搜索条件，可快速构建搜索查询语句。
POJO接口示例
容错开发说明
在编码过程中，接入系统应确认接口对Elasticsearch服务的依赖程度，并在设计Elasticsearch相关接口调用时评估容错机制，提升系统稳定性。
健康检查
接入系统不应强依赖Elasticsearch服务，推荐在设计健康检查接口时，从客户端侧增加Elasticsearch服务的可观测指标和应用健康检查接口。
可根据接入系统对Elasticsearch服务的依赖程度，设计Elasticsearch检查接口（Info定时检查），并加入应用健康检查接口，推荐将该接口增加至可观测采集，并增加告警。
应用启动禁止强依赖Elasticsearch服务，设计的健康探测接口异常时不应触发应用自动重启。
健康检查接口实现示例
异常处置
核心交易接口应保证其可靠性、鲁棒性，交易接口禁止强依赖Elasticsearch服务，使用Elasticsearch接口时应考虑应用层重试并考虑服务降级和熔断。
服务重试：接口配置自动重试，应对网络抖动等场景。
服务降级：合理设计服务降级，在超过重试次数后通过指数回避，降级访问接口。
服务熔断：合理配置失败率，防止Elasticsearch调用异常导致线程池耗尽，避免级联故障影响核心接口。
错误处理：合理捕获异常，根据错误类型打印关键日志。
异常处置示例
测试指引
接入系统在测试阶段，应规范化Elasticsearch服务相关接口测试过程，按照测试应进行功能及性能测试，推荐增加专项测试，以验证在某些故障场景下系统的应对能力，确保符合接入系统的功能要求和可用性要求。
性能测试
接入系统测试Elasticsearch相关接口性能时，推荐使用全链路性能测试，提前评估Elasticsearch容量、TPS、QPS、铺底数据，设计相关性能测试案例，确保接口符合性能要求。
专项测试
接入系统需评估Elasticsearch服务的异常切换、宕机影响，推荐在专项测试中重点评估以下场景对接入系统的影响，明确接入系统在故障过程中、故障恢复后的业务影响，可参考以下专项测试案例。
表11  专项测试案例说明
可参考上述案例，根据接入系统可用性要求补充混沌案例进行专项测试。
上线指引
接入系统在上线阶段，应从系统维度准备生产下发方案并识别风险，结合技术中台相关服务接入指引和运维单位要求，完成上线前置准备、下发检查、告警原则调整和应急卡片编写等工作。
前置资源准备
接入系统在生产环境接入Elasticsearch服务，推荐通过IT综合管理系统发起软件维护需求，在施工完成后，将反馈回执信息至申请单位。
在申请软件维护需求时，应在流程附件中提供系统概要设计说明书并明确服务资源需求，应重点关注：接入区域、服务部署模式、资源需求、容灾要求，并根据本文设计指引确定是否存在定制化需求，如配置参数等，也需在流程附件中说明。
告警原则确认
Elasticsearch服务默认接入技术中台可观测底座，提供标准化的监控、日志、告警能力。接入系统可根据业务本文设计指引，评估服务默认模板的监控项、告警阈值是否满足需求，并根据业务特点调整监控项和告警项，研发测试环境验证通过后提交至生产应用运维人员更新生产环境监控指标及告警原则。
接入前置检查
接入系统在上线或首次接入Elasticsearch服务时，应完成系统投产及维护下发前的检查核对工作，包括客户端配置确认、生产服务检查等，并根据Elasticsearch服务回执单，联系生产应用运维人员完成生产资源接入前检查，包括服务部署模式确认、生产资源确认、网络连通性确认、连接认证确认等，确保接入系统客户端配置信息准确无误。
应急卡片准备
接入系统在上线或首次接入Elasticsearch服务时，应结合Elasticsearch服务使用情况完成接入系统的应急预案（卡片）编写，并提交至生产应用运维人员。


（规范性）
指导文件
A.1  行内指导文件
本文件应符合行内指导文件要求，包括但不限于：
兴业银行，《兴业银行技术平台目录》。
兴业银行，《兴业银行软件技术平台版本序列及兼容列表》。
未注明发文号的，应遵照最新版本。
_________________________________




|  |
| --- |


| 模式 | 说明 |
| --- | --- |
| 混合模式 | 同一个Elasticsearch节点承担多种功能角色包含master、data等，该模式节点数相对较少，节省资源，但调度和计算共用资源，无法进一步拆分不同的存储节点，隔离资源。 |
| 角色分离模式 | 不同的Elasticsearch节点承担不同的功能角色，分为master节点、data节点等，该模式在后续集群扩展更加灵活，可以单独扩展某些类型的节点数量 |


| 角色名称 | 说明 |
| --- | --- |
| master节点 | 集群层面的管理，创建和删除索引、跟踪哪些节点是集群的一部分，以及决定分片分配等，因选主需要，节点数为奇数，且至少3个节点 |
| data节点 | 数据落地存储、数据增、删、改、查、缓存、聚合等操作的执行，混合模式部署时data节点数和master节点数相同；角色分离模式部署时data节点数无奇偶要求，可根据业务需求扩容节点数，节点数超5个时需在性能环境验证通过。 |
| data_hot节点 | 保存最近、最常访问的数据,仅角色分离模式支持 |
| data_cold节点 | 保存不经常访问且通常不更新的数据,仅角色分离模式支持 |
| client节点 | 不会成为主节点，也不会存储数据，只负责处理用户请求，实现请求转发，针对海量请求时进行负载均衡,仅角色分离模式支持 |


| Trandslog刷盘模式 | 说明 |
| --- | --- |
| 同步刷盘模式（默认模式） | 该模式下，每次写入、更新、删除操作后立刻执行fsync落盘，数据可靠性更强，性能较低。 |
| 异步刷盘模式 | 根据同步间隔（默认5s）周期性刷盘，性能更佳，但是数据可靠性相对低。 |


| # 具体配置测试后方可使用，需根据业务量级调整 
PUT my_index/_settings
{
  "index": {
    "refresh_interval": "1s",   
    "translog.durability": "request",       
    "translog.flush_threshold_size": "512mb"
  }
} |
| --- |


| # 具体配置测试后方可使用，需根据业务量级调整 
PUT my_index/_settings
{
  "index": {
    "refresh_interval": "30s",   
    "translog.durability": "async",       
    "translog.flush_threshold_size": "1gb"
  }
} |
| --- |


| 分词器 | 说明 | 参考使用场景 |
| --- | --- | --- |
| standard | Elasticsearch 默认分词器，按空格+标点拆分 | 英文或混合文本，非精细中文 |
| keyword | 不分词，整体索引 | 精确匹配字段，如 ID、手机号、订单号 |
| whitespace | 按空格拆分 | 英文多词短语场景，保留标点 |
| simple | 去掉标点的小写分词 | 简单英文文本 |
| language-specific | english, french, porter_stem 等 | 语言分析、词干提取 |
| ik_max_word/ik_smart | 中文分词插件 | ik_max_word 细粒度，ik_smart 粗粒度	中文搜索，全文检索 |
| pinyin | 将汉字转换为拼音索引 | 中文拼音搜索，适合姓名、城市等模糊匹配 |
| 自定义 analyzer | 可组合 tokenizer + char_filter + filter | 支持同义词、拼写纠正、停用词处理 |


| 字段 | 适用场景 | 优势 |
| --- | --- | --- |
| keyword | 精确匹配、聚合、排序 | 高性能精确查询 |
| text | 全文搜索、模糊匹配 | 支持分词与语义分析 |
| integer，long | 范围查询、统计聚合 | 高效数值计算 |
| date | 时间范围过滤、时序分析 | 支持日期表达式 |
| object | 嵌套对象 | 表达复合数据类型 |
| nested | 独立索引的嵌套对象 | 可以用于数组对象查询 |
| boolean | 布尔类型 | / |


| 查询方式 | 用途 | 特点 |
| --- | --- | --- |
| term | 精确匹配单个词条 | 不分词，适用于精确查询 |
| terms | 精确匹配多个词条 | 一次查询匹配多个值 |
| match | 全文检索，对查询字符串进行分词处理 | 支持模糊匹配和相关性评分 |
| multi_match | 在多个字段上进行全文检索 | 在多个字段上进行全文检索 |
| bool | 组合多个查询条件，支持布尔逻辑 | 灵活性高，适用于复杂查询场景 |
| match_phrase | 短语匹配，匹配查询字符串中词条的顺序和位置 | 支持设置slop，允许词条有一定的位置偏移 |
| range | 范围查询，匹配数值、日期等范围内的数据 | 支持gte、lte等条件 |
| exists | 检查字段是否存在 | 匹配包含指定字段的文档 |
| fuzzy | 模糊匹配，允许词条之间有一定的编辑距离 | 适用于拼写错误或变体词的匹配 |
| wildcard | 通配符查询，支持使用 * 和 ? 进行模糊匹配 | 适用于前缀匹配或模式匹配 |
| script | 使用脚本进行复杂的条件匹配 | 支持自定义的匹配逻辑，适用于复杂的查询需求 |


| /**
* 示例：使用_explain分析相关性评分的示例，具体地址、参数需以实际为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
*执行命令：
* curl -u user:password -X GET "http://127.0.0.1:9200/my_index/_explain?pretty" -d '
*{
*  "query": {
*    "match": {
*      "content": "search term"
*    }
*  },
*  "doc": "目标文档ID"
*}'
*/

#返回结果示例：
{
  "_index": "my_index",
  "_type": "_doc",
  "_id": "1",
  "matched": true,
  "explanation": {
    "value": 0.6931,
    "description": "weight(content:search term in 0) [PerFieldSimilarity], result of:",
    "details": [
      {
        "value": 0.6931,
        "description": "score(freq=1.0), product of:",
        "details": [
          {
            "value": 0.6931,
            "description": "idf, computed as log(1 + (N - n + 0.5)/(n + 0.5)) from field doc counts"
          },
          {
            "value": 1.0,
            "description": "tf, computed as boost * freq (freq=1.0)"
          }
        ]
      }
    ]
  }
}
/*结果分析：
_index, _type, _id: 被解释的文档信息。
matched: 是否匹配查询，true 表示匹配。
explanation: 详细解释，包括评分计算过程。
相关性评分由 idf 和 tf 两个因素决定：
idf (Inverse Document Frequency): 衡量一个词在 corpus 中的重要性。词越稀有，idf 越高。
tf (Term Frequency): 衡量一个词在文档中出现的频率。词频越高，tf 越高。
示例中总评分 = idf * tf = 0.6931 * 1.0 = 0.6931。*/ |
| --- |


| /**
* 示例：使用_profile 优化查询执行的示例，具体地址、参数需以实际为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
*执行命令：
* curl -u user:password -X GET "http://localhost:9200/my_index/_search?pretty&_profile=true" -d '
*{
*  "query": {
*    "match": {
*      "content": "search term"
*    }
*  }
* }'
*/

#返回结果示例：
"profile": {
  "shards": [
    {
      "id": "my_index-0",
      "search_type": "DFS_QUERY_THEN_FETCH",
      "total_time_in_nanos": 123456,
      "total_time_in_nanos_for_suggestions": 0,
      "total_shard_time_in_nanos": 123456,
      "breakdown": {
        "parse": {
          "time_in_nanos": 1234
        },
        "query": {
          "time_in_nanos": 5678
        },
        "fetch": {
          "time_in_nanos": 9876
        }
      }
    }
  ]
}
/*结果说明：
total_time_in_nanos: 查询的总执行时间（纳秒）。
breakdown: 查询执行的各个阶段的时间分配，包括解析（parse）、查询（query）和获取（fetch）。
优化建议：
如果 parse 时间较长，可能存在语法错误或复杂的查询结构，简化查询。
如果 query 时间较长，可能存在过多的分片或分片不平衡，考虑调整分片数量。
如果 fetch 时间较长，可能存在过多的文档返回，考虑分页或优化返回字段。*/ |
| --- |


| 版本 | 说明 |
| --- | --- |
| 7.17+ | 根据我行开源技术目录选择Elastisearch服务端版本，以最新开源技术目录为准。 |
| 8.12+ | 根据我行开源技术目录选择Elastisearch服务端版本，以最新开源技术目录为准。 |


| 客户端类型 | 版本要求 | 说明 |
| --- | --- | --- |
| co.elastic.client:elasticsearch-java | 与服务端版本保持一致 | 使用ElasticSearch7推荐使用elasticsearch-java 7.17+版本 |
| co.elastic.client:elasticsearch-java | 与服务端版本保持一致 | 使用ElasticSearch8推荐使用elasticsearch-java 8.12+版本 |


| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| JVM配置 | 根据服务资源动态配置 | Xms=Xmx=最大内存(Limit内存)/2
MaxDirectMemorySize=最大内存(Limit内存)/4 |
| cluster.routing.allocation.enable | all | 自动分片分配策略所有分片开启 |
| bootstrap.memory_lock | false | 开启后会在启动时锁定内存，无需修改生产环境关闭swap |
| index.number_of_shards | 1 | 索引创建默认分片数，创建索引时需调整，否则使用模式值 |
| index.number_of_replicas | 1 | 索引创建默认副本数，创建索引时需调整，否则使用模式值 |
| index.refresh_interval | 1s | 索引创建默认刷新时间，创建索引时需调整，否则使用模式值 |


| 参数 | 默认值 | 参数说明 | 配置建议 |
| --- | --- | --- | --- |
| maxConnTotal | 10 | 连接池大小 | 1.不建议设置为默认值
2.建议根据接入系统并发度及性能测试结果确认配置为50到200 |
| maxConnPerRoute | 10 | 单台目标主机最大连接数 | 1.不建议设置为默认值
2.建议配置为maxConnTotal/2 |
| connectTimeout | 1000ms | 建立连接超时时间 | 1.根据项目组业务需求确认 |
| socketTimeout | 30000ms | 等待数据响应的超时时间 | 1.根据项目组业务需求确认
2.写多读少场景可参考性能测试数据调整为60000ms,请求需满足应用系统对外接口要求并通过性能测试后方可调整 |
| maxRetryTimeoutMillis | 30000ms | 请求失败后重试的最大等待时间 | 1.配置为socketTimeout一致 |
| CompressionEnabled | false | 压缩数据 | 1.大批量写入或大文档时开启 |


| /**
* 示例：创建新的索引，项目组使用前请测试验证，实际配置以项目组使用服务为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 描述：使用REST API创建一个ES索引
* 说明：根据设计需要设置分片数、落盘配置，索引分词的配置
*/
PUT /products
{
  "settings": {
   "refresh_interval": "1s",   
   "translog.durability": "request",       
   "translog.flush_threshold_size": "512mb",
   "number_of_shards": 12,   
     "number_of_replicas": 1, 
    "analysis": {
      "filter": {
        "pinyin_filter": {
          "type": "pinyin",
          "keep_full_pinyin": true,
          "keep_joined_full_pinyin": true,
          "keep_original": true,
          "lowercase": true,
          "keep_separate_first_letter": false  // 不需要的选项可关闭
        },
        "my_synonyms": {
          "type": "synonym",
          "synonyms": [
            "手机, 手持电话，mobile，tel，phone",
            "电脑, 计算机，computer"
          ]
        }
      },
      "analyzer": {
        "products_analyzer": {
          "tokenizer": "keyword",
          "filter": ["pinyin_filter", "my_synonyms"]
        },
        "search_analyzer": {
          "tokenizer": "ik_smart",
          "filter": ["lowercase", "my_synonyms"]
        },
        "index_analyzer": {
          "tokenizer": "ik_max_word",
          "filter": ["lowercase", "my_synonyms"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "products_analyzer",
"search_analyzer": "search_analyzer",
        "fields": {
          "keyword": { "type": "keyword" },   //用于排序和聚合
          "text": {                           //用于中文分词
            "type": "text",
            "analyzer": "index_analyzer",
"search_analyzer": "search_analyzer"
}
        }
      }
    }
  }
} |
| --- |


| /**
* 示例：创建新的索引模板，项目组使用前请测试验证，实际配置以项目组使用服务为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 描述：使用REST API创建一个ES索引模板
* 说明：根据设计需要设置分片数、落盘配置，索引分词的配置
*/
PUT /_index_template/user_template
{
  "index_patterns": ["users-*"],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "refresh_interval": "30s",
      "analysis": {
        "filter": {
          "pinyin_filter": {
            "type": "pinyin",
            "keep_full_pinyin": true,
            "keep_joined_full_pinyin": true,
            "keep_original": true,
            "lowercase": true
          }
        },
        "analyzer": {
          "user_name_analyzer": {
            "type": "custom",
            "tokenizer": "keyword",
            "filter": ["pinyin_filter", "lowercase"]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "name": {
          "type": "text",
          "analyzer": "user_name_analyzer",        // 使用自定义拼音分词器
          "fields": {
            "keyword": { "type": "keyword" }
          }
        },
        "email": {
          "type": "keyword"
        },
        "bio": {
          "type": "text",
          "analyzer": "ik_max_word",               // 使用 IK 中文分词
          "search_analyzer": "ik_smart"
        },
        "age": {
          "type": "integer"
        },
        "created_at": {
          "type": "date"
        }
      }
    },
    "aliases": {
      "all_users": {}
    }
  }
} |
| --- |


| /**
* 示例：创建Es-JAVA客户端，项目组使用前请测试验证，实际代码以项目组客户端版本为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 类描述：使用创建一个Es-JAVA客户端
* 说明：用于初始化客户端
*/
@Configuration
public class ElasticsearchClientConfig {

    @Bean(destroyMethod = "close")
    public ElasticsearchClient elasticsearchClient() {
        // basic auth验证
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        // 访问用户名和密码为您Elasticsearch实例时设置的用户名和密码。
        credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(login, password));
        RestClientBuilder builder = RestClient.builder(
                new HttpHost("change me", 9200, "http"))
            .setRequestConfigCallback(requestConfigBuilder ->
                requestConfigBuilder
                    .setConnectTimeout(5000)
                    .setSocketTimeout(60000)
                    .setConnectionRequestTimeout(3000)
            )
            .setHttpClientConfigCallback(httpClientBuilder ->
                httpClientBuilder
                    .setMaxConnTotal(200)
                    .setMaxConnPerRoute(100)
                    .disableAuthCaching()
                    .setKeepAliveStrategy((response, context) -> 30_000)
            )
            .setFailureListener(new RestClient.FailureListener() {
                @Override
                public void onFailure(Node node) {
                    System.err.println("节点不可用: " + node);
                }
            })
            .setCompressionEnabled(true)
.setDefaultCredentialsProvider(credentialsProvider));

        RestClient restClient = builder.build();
        ElasticsearchTransport transport = new RestClientTransport(restClient, new JacksonJsonpMapper());
        return new ElasticsearchClient(transport);
    }
} |
| --- |


| /**
* 示例：Springboot-data客户端配置，项目组使用前请测试验证，实际代码以项目组客户端版
* 本为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 类描述：springboot-data客户端配置
* 说明：用于初始化客户端
*/

spring:
  elasticsearch:
    uris: http://localhost:9200
    # 认证配置，此处仅示例，使用时需调整为实际认证方案，复核
    username: elastic
    password: your_password_here
    # 参考客户端配置调整：连接超时
    connection-timeout: 5000ms
    socket-timeout: 10000ms
-------------------------------------------------------------------------------------
/**
* 示例：创建Springboot-data客户端，仅供参考，如需使用请经过测试验证
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 类描述：使用创建一个Springboot-data客户端
* 说明：自定义客户端示例，开启调整连接池大小时可参考自定义客户端
*/

Configuration
@EnableElasticsearchRepositories
public class ElasticsearchConfig {

    @Value("${spring.elasticsearch.uris}")
    private String uris;

    @Value("${spring.elasticsearch.username}")
    private String username;

    @Value("${spring.elasticsearch.password}")
    private String password;

    @Bean
    public ElasticsearchClient elasticsearchClient() {
        // 创建 HTTP 客户端
        HttpClient httpClient = HttpAsyncClient.builder()
            .setMaxConnTotal(30)
            .setMaxConnPerRoute(10)
            .setKeepAliveStrategy(new DefaultConnectionKeepAliveStrategy())
            .setDefaultCredentialsProvider(credentialsProvider())
            .build();

        // 创建传输层
        RestClientTransport transport = new RestClientTransport(
            httpClient,
            new JacksonJsonpMapper()  // 使用 Jackson 序列化
        );

        // 创建 Elasticsearch 客户端
        return new ElasticsearchClient(transport);
    }

    private CredentialsProvider credentialsProvider() {
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
            AuthScope.ANY,
            new UsernamePasswordCredentials(username, password)
        );
        return credentialsProvider;
    }

    @Bean
    public ElasticsearchTemplate elasticsearchTemplate(ElasticsearchClient client) {
        return new ElasticsearchTemplate(client);
    }
} |
| --- |


| /**
* 示例：创建索引，项目组使用前请测试验证，实际代码以项目组客户端版本为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 类描述：Elasticsearch索引管理类
* 说明：用于创建索引、索引删除
*/

public class ManageIndex {
@Autowired
ElasticsearchClient esClient;
      
//创建索引方法
    public void createIndex(UserIndex data) {
        try {
         // Index的mapping配置
            Map<String, Property> properties = data.getMappingProperties()

            CreateIndexRequest req = CreateIndexRequest.of(c -> c
                    .index("articles")
                    .mappings(m -> m
                            .properties(properties)
                    )
                    .settings(s -> s
                            .numberOfReplicas(data.getReplica())  // 副本数
                            .numberOfShards(data.getShards())    // 分片数
                    )
            );            
boolean created = esClient.indices().create(req).acknowledged(); 
        } catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
    }

//删除索引方法
    public void removeIndex(UserIndex data) {
        try {
            // 删除索引
            DeleteIndexResponse deleteIndexResponse = client.indices().delete(e -> e.index(data.getName()));        
} catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
    }

//查询索引方法
    public UserIndex queryIndex(String name) {
        try {
            // 查询索引
            GetIndexResponse getIndexResponse = client.indices().get(e -> e.index(name));     
} catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
// 实际业务中，这里需要根据业务调整为对象转换逻辑
          return generateIndex(getIndexResponse);
    }
} |
| --- |


| /**
* 示例：创建文档，项目组使用前请测试验证，实际代码以项目组客户端版本为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 类描述：Elasticsearch创建文档类
* 说明：用于创建文档、删除文档、更新文档、查询文档
*/

//创建User对象
@Data
@AllArgsConstructor
@NoArgsConstructor
public class User {
    private String name;
    private String sex;
    private Integer age;
    private String id；
}
public class ManageDocument {
 @Autowired
ElasticsearchClient esClient;

//创建文档
    public boolean createUser(User data，Index index) {
        try {
CreateResponse created = esClient.create(e->e.index(index.getName()).id(data.getId()).document(data)); 
        } catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
          return true
    }

//查询文档
    public User getUserDocument(String id，Index index) {
        try {
GetResponse<UserDocument> result= esClient.get(e->e.index(index.getName()).id(id),UserDocument.class); 
        } catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
          return result.source();
    }

//删除文档
    public boolean removeUser(User data，Index index) {
        try {
DeleteResponse rep= esClient.delete(e->e.index(index.getName()).id(data.getId())); 
        } catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
return true;
    }

//分页搜索
    public List<User> pageingQueryUser(Query data，Index index) {
        List<User> users = new ArrayList<User>();
        try {
            // 分页查询
            SearchResponse<User> searchResponse = client.search(
                s -> s.index(index.getName())
                        .query(q -> q.matchAll(m -> m))
                        .from(data.getFrom())
                        .size(data.getSize())
                , User.class);  
            searchResponse.hits().hits().forEach(h -> users.add(hit.source())); 
} catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
return users;
    }

//组合查询搜索
    public List<User> combinationQueryUser(Query data，Index index) {
        List<User> users = new ArrayList<User>();
        try {
            // 组合查询
            SearchResponse<User> searchResponse = client.search(
                s -> s.index(index.getName()).query(q -> q.bool(b -> b
                        .must(m -> m.match(u -> u.field("age").query(data.getAge())))
                        .must(m -> m.match(u -> u.field("sex").query("男")))
                        .mustNot(m -> m.match(u -> u.field("sex").query("女")))
                ))
                , User.class);
            searchResponse.hits().hits().forEach(h -> users.add(hit.source())); 
} catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
return users;
    }

//模糊查询搜索
    public List<User> combinationQueryUser(Query data，Index index) {
        List<User> users = new ArrayList<User>();
        try {
            // 模糊查询，fuzziness表示差几个可以查询出来
            SearchResponse<User> searchResponse = client.search(s->s.index(index.getName())
.query(q -> q.fuzzy(f -> f.field("name")
.value(data.getName()).fuzziness(data.getFuzzy())))
                , User.class);        
searchResponse.hits().hits().forEach(h -> users.add(hit.source())); 
} catch (Exception e) {
            // 实际业务中，这里需要对异常进行具体处理，例如记录日志等 
        } finally {
            // 实际业务中，这里需要进行其他具体操作，例如打印日志
        }
return users;
    }
} |
| --- |


| /**
* 示例：抽象文档Respository接口，项目组使用前请测试验证，实际代码以项目组客户端版
* 本为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 接口描述：Elasticsearch文档Respository接口
* 说明：通过Respository接口，可以直接在Service层调用
*/
public interface ProductRepository extends ElasticsearchRepository<Product, String> {

    // 根据名称模糊查询
    List<Product> findByNameContaining(String name);

    // 根据类别查询
    List<Product> findByCategory(String category);

    // 自定义查询
    @Query("{\"bool\": {\"must\": [{\"match\": {\"name\": \"?0\"}}, {\"range\": {\"price\": {\"lte\": ?1}}}]}")
    List<Product> findByNameAndMaxPrice(String name, Double maxPrice);
} |
| --- |


| /**
* 示例：健康检查接口，项目组使用前请测试验证，实际代码以项目组客户端版本为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 接口描述：Elasticsearch健康检查接口
* 说明：服务异常不影响应用，仅上报状态对接监控及告警
*/
@Component
public class ElasticsearchHealthIndicator implements HealthIndicator {

    @Autowired
    private ElasticsearchClient client;

    @Override
    public Health health() {
        try {
            HealthResponse health = client.cluster().health();
            String status = health.status().jsonValue();

            if ("green".equals(status)) {
                return Health.up()
                    .withDetail("cluster_name", health.clusterName())
                    .withDetail("status", status)
                    .withDetail("nodes", health.numberOfNodes())
                    .build();
            } else if ("yellow".equals(status)) {
                return Health.warn()
                    .withDetail("status", status)
                    .withDetail("unassigned_replicas", health.unassignedShards())
                    .build();
            } else {
                return Health.down()
                    .withDetail("status", status)
                    .withDetail("unassigned_shards", health.unassignedShards())
                    .build();
            }
        } catch (Exception e) {
            return Health.down().withException(e).build();
        }
    }
} |
| --- |


| /**
* 示例：异常处置、重试、降级，项目组使用前请测试验证，实际代码以项目组客户端版本
* 为准
* @author 技术中台服务岗
* @version 1.0 2025-8-1
* 接口描述：Elasticsearch调用接口时异常处置、重试、降级示例
* 说明：根据Resilience4j框架实现，如使用其余框架根据对应框架规范实现相关功能
*/
@Service
public class ProductSearchService {

    @Autowired
    private ElasticsearchClient esClient;

    // 搜索方法：带熔断、重试、降级
    @CircuitBreaker(name = "esSearch", fallbackMethod = "fallbackSearch")
    @Retry(name = "esSearch", fallbackMethod = "fallbackSearch")
    public List<Product> searchProducts(String keyword) throws IOException {
        SearchResponse<Product> response = esClient.search(s -> s
                .index("products")
                .query(q -> q.match(m -> m.field("name").query(keyword))),
            Product.class
        );

        return response.hits().hits().stream()
            .map(hit -> hit.source())
            .toList();
    }

    // 降级方法（熔断或超过重试失败后调用）
    public List<Product> fallbackSearch(String keyword, Exception e) {
        System.warn("Elasticsearch search fallback due to: " + e.getMessage());
        // 根据业务要求，可返回缓存数据、静态数据、空列表直接降级
// 也可调整为降级接口，从缓存或数据库中获取，性能降低但是服务保持可用
        return Collections.emptyList(); 
    }

    // 也可为 IOException 单独定义降级
    public List<Product> fallbackSearch(IOException e) {
        System.warn("Fallback due to IO error: " + e.getMessage());
        return Collections.emptyList();
    }
} |
| --- |


| 专项测试案例 | 测试说明 |
| --- | --- |
| ES单个data节点宕机 | 本场景模拟Es data单个节点宕机，经故障处置恢复后应用是否可自动重连以及业务代码正确重新查询、创建 |
| ES单个master节点宕机 | 本场景模拟Es master单个节点宕机，经故障处置恢复后应用是否可自动重连以及业务代码正确重新查询、创建 |
| ES全量data节点宕机 | 本场景模拟Es data全量节点宕机，经故障处置恢复后应用是否可自动重连以及业务代码正确重新查询、创建 |
| ES全量master节点宕机 | 本场景模拟Es master全量节点宕机，经故障处置恢复后应用是否可自动重连以及业务代码正确重新查询、创建 |
| ES节点网络延迟演练 | 本场景模拟应用端Es网络延迟导致通信异常出现数据丢失场景，验证应用是否具备写入失败重试的能力，验证是否具备补偿能力 |
| ES节点网络丢包演练 | 本场景模拟应用端到Es网络丢包导致通信异常出现数据丢失场景，验证应用是否具备写入失败重试的能力，验证是否具备补偿能力 |
