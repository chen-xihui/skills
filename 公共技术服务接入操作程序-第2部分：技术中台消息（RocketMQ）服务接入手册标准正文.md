Q/CIB
兴业银行股份有限公司企业标准
Q/CIB 4052.2—2024


公共技术服务接入操作程序 第2部分：
技术中台消息服务接入手册
Public technical service access operation procedures—Part2:
technical central platform messaging service access handbook

2024-10-30发布
2024-10-30实施
兴业银行股份有限公司发布
ICS 35.240.40
CCS A11


目  次
目次	Ⅰ
前言	Ⅲ
1 范围	1
2 规范性引用文件	1
3 术语和定义	1
4 缩略语	4
5 基本概念	5
5.1 部署模式	5
5.2 持久化说明	5
5.3 消息复制说明	5
5.4 消息清理策略	6
5.5 消息类型	6
6 消息服务	6
6.1 服务特点	6
6.2 服务模式	7
6.3 服务容灾	7
7 设计指引	7
7.1 消息服务依赖	7
7.2 数据隔离	7
7.3 部署模式	8
7.4 部署区域	8
7.5 功能接口设计	9
7.6 容错设计	11
7.7 容灾设计	11
8 开发指引	12
8.1 服务端版本要求	12
8.2 客户端版本要求	12
8.3 客户端配置	13
8.4 生产者开发说明	16
8.5 消费者开发说明	26
8.6 安全编码	29
9 测试指引	29
9.1 性能测试	29
9.2 专项测试	29
10 上线指引	30
10.1 前置资源准备	30
10.2 告警规则确认	30
10.3 接入前置检查	30
10.4 应急卡片准备	30
附录A（规范性） 指导文件	31

前  言
本文件按照GB/T1.1—2020《标准化工作导则第1部分：标准化文件的结构和起草规则》给出的规则起草。
本文件由兴业银行科技管理部提出并归口。
本文件起草单位：兴业数字金融服务（上海）股份有限公司。
本文件主要起草人：杨涛、林鑫、王畅。
本文件为首次发布。
公共技术服务接入操作程序
第2部分：技术中台消息服务接入手册
范围
本文件给出了接入系统使用消息服务时应遵循的设计原则、编码规范、测试要求，引导接入系统合理、高效地使用公共技术服务，提升应用的稳定性与可维护性。
本文件适用于全集团具有研发、运维职能的单位。
规范性引用文件
本文件没有规范性引用文件。
术语和定义

技术中台  technical middleoffice
将本行公共的、通用的关键基础技术资源集中建设和维护，以平台形式提供技术服务。
技术中台包括应用开发平台、Devops与研发保障、应用集成、微服务支撑与治理、数字化运营与支撑、通用技术服务、基础PaaS、容器云平台八大板块。

技术中台消息（RocketMQ）服务  technical middleoffice messaging(RocketMQ) service
消息服务
技术中台基于云原生Operator技术，将RocketMQ软件实现PaaS化，并作为一类基础技术服务进行提供，具备按需申请、快速交付、局部故障自愈和高可用性等特性。
根据JR/T0166—2020定义，PaaS（platformasaService，平台即服务）为云服务类别中的一种。
Operator是一种用于管理Kubernetes集群中复杂应用的工具，基于Kubernetes的控制器，自动化复杂应用的部署、管理和运维过程。

RocketMQ“消息，事件，流”实时数据处理平台  RocketMQ "messaging,eventing,streaming" real-time dataprocess platform
RocketMQ
一种开源分布式消息传递系统，具备高性能、高吞吐的特性支持各类消息传递模型，适用于大规模分布式系统中消息通信。
来源自RocketMQ第三方开源运营网址，https://rocketmq.apache.org，相关定义有修改。


RocketMQ消息代理组件  RocketMQ Broker
Broker
RocketMQ中的消息存储节点，负责消息的存储、传输以及查询等功能，分为Master和Slave两种角色，具备高性能、高可用性等特点。

RocektMQ消息命名组件  RocketMQ NameServer
NameServer
RocketMQ中负责接收Broker的注册请求，为Producer和Consumer提供接入访问，并定期维护集群元数据、Broker健康状态的组件，具备高性能、高可用性等特点。

RocketMQ生产者  RocketMQ Producer
生产者  Producer
RocketMQ中用来构建并传输消息到服务端的运行实体，负责消息生产及发送，通常被集成在业务系统中，将业务消息按照要求封装并发布至服务端。

RocketMQ生产者组  RocketMQ ProducerGroup
生产者组  ProducerGroup
RocketMQ生产者的集合，具备一致生产者行为的分组，与生产者不同，生产者组并不是运行实体，而是一个逻辑资源，通过生产者组内多个生产者同时生产消息，实现水平扩展、高可用特性。

RocketMQ消费者  RocketMQ Consumer
消费者  Consumer
RocketMQ中用来接收并处理消息的运行实体，通常被集成在业务系统中，从服务端获取消息，并将消息转化为业务可理解的信息，供业务逻辑处理。

RocketMQ消费者组  RocketMQ ConsumerGroup
消费者组  ConsumerGroup
RocketMQ消费者的集合，承载多个消费行为一致的消费者的负载均衡分组，和消费者不同，消费者组并不是运行实体，而是一个逻辑资源，通过消费者组内多个消费者，实现消费性能的水平扩展和高可用特性。

RocketMQ消息  RocketMQ Message
消息  Message
RocketMQ中的最小数据传输单元，生产者、消费者将业务数据的负载和拓展属性包装为消息进行传输。

RocketMQ消息类型  RocketMQ MessageType
消息类型  MessageType
RocketMQ根据消息传输特性的不同而定义的分类，支持普通消息、顺序消息、事务消息、延时消息。

RocketMQ消息标签  RocketMQ MessageTag
标签  Tag
RocketMQ提供的细粒度消息分类属性，可在主题层级之下做消息类型的细分。消费者通过订阅特定的标签来实现细粒度过滤。

RocketMQ主题  RocketMQ Topic
主题  Topic
RocketMQ中传输消息和存储的顶层组件，用于标识同一类逻辑消息。

RocketMQ消息队列  RocketMQ MessageQueue
队列  Queue
RocketMQ中存储、传输消息的实际组件，也是消息的最小存储单元，所有主题均由多个队列组成，通过队列的水平拆分和队列内部的流式存储，实现高可用特性。

RocketMQ消费位点  RocketMQ ConsumerOffset
位点  Offset
RocketMQ消费者组最新一条消费消息的记录，消费者在消费消息后不会立刻从队列中删除消息，通过消费位点可定位消费者可消费的下一条消费。

RocketMQ推送消费模式  RocketMQ PushConsumer
PushConsumer
RocketMQ提供的一种消费模式，服务端主动推送消息给消费者，对消息队列负载均衡、消息进度自动提交、消费重试进行了封装，提供统一的API，通常用于消息可靠性场景使用。

RocketMQ拉取消费模式  RocketMQ PullConsumer
PullConsumer
RocketMQ提供的一种消费模式，消费者主动从服务端拉取消息，通常用于消费者需要灵活处置消息场景使用。

RocketMQ消息堆积  RocketMQ MessageBacklog
消息堆积
RocketMQ生产者消息已发送到服务端，但由于消费者的消费能力有限，未能在短时间内将所有消息正确消费掉，此时在服务端保存着未被消费的消息，该状态即消息堆积。

RocketMQ集群模式消费  RocketMQ ClusteringMode Consume
集群消费
RocketMQ消费者组内每个消费者实例平均分配消息，消费者组内的消费者不会重复处理消息。

RocketMQ广播模式消费  RocketMQ BroadcastingMode Consume
广播消费
RocketMQ消费者组内每个消费者实例接收并处理全量消息。

RocketMQ数据流传输  RocketMQ Connect
Connect
RocketMQ提供的用于数据流传输的工具，具备可靠性、可扩展性，支持从RocketMQ作为源端或目的端进行数据传输。

缩略语
下列缩略语适用于本文件。
TPS：每秒事务处理数（TransactionsPerSecond）
JSON：JS对象简谱（JavaScriptObjectNotation）
XML：可扩展标记语言（eXtensibleMarkupLanguage）
DNS：域名系统（DomainNameSystem）
基本概念
部署模式
RocketMQ作为消息传输中间件，可提供单点模式、主从模式、Deleger高可用模式三种不同的部署模式，具体可见表1。
表1  部署模式分类
持久化说明
RocketMQ使用二进制文件实现消息、元数据的持久化存储，在性能和数据持久化方面较为均衡，可支持同步刷盘和异步刷盘机制，接入系统可根据性能要求和可用性要求等要求综合考虑，确认消息落盘模式，具体可见表2。
表2  消息落盘模式分类
消息复制说明
消息服务Broker的复制机制是高可用的关键能力，在消息在发送到Broker主节点后会复制到Broker从节点，接入系统可根据可用性要求等要求综合考虑，确认消息复制模式，具体可见表3。
表3  消息复制模式分类
消息清理策略
RocketMQ提供默认消息过期清理策略，接入系统可根据消息重要程度评估存储大小和消息过期清理时间，确认消息过期清理时间参数，默认过期清理时间为3天，消息过期清理策略具体可见表4。
表4  消息过期清理策略

消息类型
RocketMQ支持多种消息类型，接入系统可根据使用场景选择匹配的消息类型，具体可见表5。
表5  消息类型
消息服务
服务特点
消息服务提供了高效管理消息实例生命周期的能力，可快速部署、配置、管理RocketMQ服务实例，接入系统无需关注底层部署服务器资源及技术细节，应重点关注如何正确、合理地使用消息能力，消息服务具备以下特性。
快速交付：支持服务按需申请快速交付，按需横向扩容或纵向扩容。
信创适配：支持鲲鹏、海光芯片、麒麟操作系统，具备全栈信创支持能力。
服务高可用：可在服务器宕机等异常场景时，自动实现主从节点切换、集群元数据、Broker健康状态自动更新，保障服务的高可用。
多维度监控：支持集群事件监控、运行态监控、日志监控等多维度立体监控，实时掌握集群健康状态。
功能完备：支持顺序、事务等消息类型及消息重试机制，并提供延迟消息、失败重试、死信队列等多种灵活的消息处理策略，支持可视化消息查询、消息轨迹追踪等功能。
服务模式
消息服务提供两种部署架构：普通消息模式和顺序消息模式，两者均基于Dleger高可用模式实现数据备份和故障场景下快速切换，接入系统应根据两类模式特点，结合实际需求进行模式选择。
普通消息模式：
基于Dleger高可用模式提供服务，默认配置为2个主节点和4个从节点，在该模式下支持根据消息数据量扩展Broker分片。
此模式下RocketMQ会将主题的队列分散到不同的Broker，提升系统的吞吐量和容错能力，异常情况下会对故障Broker分片进行主从切换。
顺序消息模式：在普通消息模式的基础上增加全局顺序消息功能，保障全局消息顺序一致，接入系统如使用顺序消息应选择该模式。
服务容灾
消息服务提供同城、异地跨机房的数据同步能力和单元化同步能力，支撑接入系统同城双活、异地灾备、单元化建设，接入系统应根据业务需求选择容灾同步能力。
数据同步能力：消息服务基于RocketMQ Connect组件进行增强，实现跨RocketMQ集群间数据同步能力，支持消息过滤、顺序同步、流量回环识别等功能。
单元化能力：消息服务对接JUP开发平台，基于原生RocketMQ客户端进行增强，支持单元化消息路由，生产者可跨单元投递消息。
设计指引
接入消息服务时，在系统设计阶段应重点设计消息队列依赖、Topic拆分、消息发送要求、消息消费要求等。
消息服务依赖
消息服务作为系统解耦、消息异步传递的核心组件，接入系统应解耦应用和消息服务，在初始化启动、核心交易接口设计时不能强依赖消息服务，推荐通过异步初始化、异常捕获等设计保障核心交易接口稳定。
数据隔离
接入系统推荐在本系统范围内使用消息服务，不宜多个系统混用消息服务，可根据业务需求拆分消息服务、主题、生产者消费者。
消息服务拆分
消息数据应根据系统可用性等级、数据重要等级，设计Topic、消费者、生产者承载的消息业务并进行消息拆分设计，可参考以下拆分规则。
根据数据可用性等级拆分消息数据至多套消息服务（例如某系统的支付模块和监控模块使用两套消息服务）。
根据性能要求拆分消息数据至多套消息服务。
主题拆分
接入系统使用消息服务时，推荐根据业务模型、消息分类进行主题拆分设计，可参考以下拆分规则。
根据业务领域拆分消息数据至多个主题（例如用户消息、订单消息分别拆分不同主题）。
根据消息类型拆分消息数据至多个主题，单个主题下的消息类型应该保持一致（例如普通消息、事务消息使用不同主题）。
生产者及消费者拆分
接入系统使用消息服务时，推荐根据业务逻辑拆分多个生产者组、消费者组，可参考以下拆分规则。
单一应用组件不应同时承载生产者和消费者职责，生产者和消费者推荐拆分为不同运行实体。
根据数据来源拆分生产者组，多个数据来源推荐由不同生产者组承载。
根据消息用途拆分消费者组，应确保每个消费者组业务逻辑独立，避免消费相互干扰。
根据可扩展性拆分生产者组、消费者组，推荐设计独立的生产者和消费者组件，可快速横向扩容生产者、消费者。
部署模式
性能及数据量
接入系统应根据消息保存时间、消息生产TPS、消息体大小估算存储空间，单个Broker存储空间=（消息保存时间*消息体大小*消息生产TPS*24*60*60）/0.7/消息服务分片数，可参考以下服务规格选型。
低配版本：建议TPS低于500且消息体1k以内的系统使用，Broker资源2C/4G/30G存储（2分片，1主2从），NameServer资源2C/4G（2副本），单个分片存储数据使用上限200G。
标准版本：建议TPS在500至2000且消息体10k以内的系统使用，Broker资源4C/8G/50G存储（3分片，1主2从），NameServer资源4C/8G（2副本），存储数据使用上限500G。
高配版本：建议TPS在2000以上的系统使用，Broker资源8C/16G/200G存储（分片数=2n+1，n≥1，1主2从），NameServer资源4C/8G（3副本），存储数据使用上限1000G。
消息持久化
接入系统应根据功能、可用性需求选择消息的持久化设计，并设计生产者、消费者消息处理容错功能，可参考以下持久化分析选型。
服务端持久化设计：非易失消息传输场景下，配置同步刷盘模式（默认未开启），推荐使用Dledger复制模式（默认开启）。
生产者持久化设计：非易失消息传输场景下，生产者确保发送消息数据源可重复获取，推荐在消息发送异常时存储消息至数据库，并在业务侧设计消息重发，避免消息发送失败导致数据丢失。
其他
除上述参考设计外，接入系统可参考其余非功能需求指标选型。
部署区域
接入系统应合理选择部署区域，可参考以下原则选择。
接入系统与消息服务推荐部署至相同网络安全域，避免跨网络域访问。
灾备、双活架构系统，应使用相同架构、规格的消息服务。
消息服务访问地址不能发布至公网。
功能接口设计
消息设计
消息服务设计功能接口时，应根据业务场景设计消息的数据结构、消息类型、消息接口功能和安全设计，可参考以下设计。
消息结构设计，推荐根据业务需求设计消息的结构、大小、生命周期：
消息头设计时，MessageID、Topic无需额外设计，Tag作为消息标签可根据业务属性进行设计用于消息分类和筛选。
消息体设计时，如存在结构化数据可使用JSON、XML存储。
消息类型设计，应根据业务特性选择普通消息、顺序消息、事务消息和延时消息，并确保同一主题处理同一类消息。
消息功能设计，应评估消息大小、消息易失性、消息幂等性和性能指标：
消息大小：单条消息大小推荐在4MB以内，如使用批量消息，每批消息总量推荐在4MB以内。
消息易失性：根据消息重要程度，非易失消息传输时，应设计消息发送前落盘或落库，当消息发送失败时，推荐设计重试逻辑、补偿任务等方案确保消息不丢失。
消息幂等性：消息多次发送时，应保障消息幂等性，推荐在消息体中增加消息ID或使用Key标识消息体，消费者可通过具体标识识别重复消息。
消息性能：对于超过4K的消息体应压缩消息后再发送，推荐使用LZ4和ZLIB压缩算法。
消息安全设计，传输敏感消息时，应在应用层对消息加密再发送。
主题及队列设计
功能接口设计时，对使用消息服务的主题和队列能力进行相关设计，应评估主题设计的易用性、可维护性和性能，可参考以下设计。
主题命名规范：以字母开头，长度在1—63个字符间，由小写字母、数字和下划线组成的字符串，主题命名应要清晰表达业务含义，如存在跨系统消息传输推荐在主题命名中体现生产者的系统编码（例如订单主题可命名为j036x0_order）。
主题队列数量规范：
非顺序消息默认配置为4，最小配置为2，应根据消息处理要求设计主题队列数量，主题队列数量应大于该主题消费者数。
顺序消息全局顺序场景应配置为1。
生产者设计
接入消息服务时，设计生产者应用，应根据业务发送消息重要程度进行设计，保障生产者的可维护性、性能和稳定性，可参考以下设计。
生产者组命名规范：以字母开头，长度为1—63个字符，由字母、数字和下划线组成的字符串，生产者组命名清晰表达业务含义，如存在跨系统消息传输推荐体现生产者组系统编码（例如订单消息发送生产者可命名为pg_j036x0_order）。
生产者消息发送规范：
同步发送：适用于对消息发送结果有严格要求的场景，应确保发送异常可捕获，常用于支付、订单处理等关键业务场景。
异步发送：适用于对响应速度要求高但对发送结果不敏感的场景，异步发送不会阻塞主流程业务，推荐通过异步回调处理异常。
生产者消息发送设计：
同一生产者组下的生产者实例应确保发送消息主题完全一致。
生产者发送消息建议根据服务端负载均衡，将消息分散发送到不同Broker实例，避免指定队列发送消息。
生产者应限制消息发送并发度，防止消息发送过快导致应用过载或Broker负载过重。
推荐根据业务场景使用批量发送功能，处理同一个主题的消息。
消费者设计
接入消息服务时，设计消费者应用，应根据业务场景设计消息处理逻辑，确保消费者的可维护性、性能和稳定性，可参考以下设计。
消费者组命名规范：以字母开头，长度为1—63个字符，由字母、数字和下划线组成的字符串，消费者组命名清晰表达业务含义，如存在跨系统消息传输推荐体现消费者组系统编码（例如订单消息消费者可命名为cg_j036x0_order）。
消费模式设计，应根据业务情况选择拉取消费或推送拉取消费：
推送消费模式：适用于消费频率有严格控制的场景，该模式下消息获取、负载均衡、消费位点自动提交、消费重试等能力统一进行了封装，推荐使用该模式。
拉取消费模式：适用于实时性要求高的业务场景。
消费者消息处理设计：
同一消费者组下的消费者实例应确保主题、消息标签完全一致。
应确保消息处理逻辑简单高效、避免长时间阻塞，不推荐直接调用第三方接口等耗时较长的逻辑，推荐使用异步方式调用。
消费者应根据消息处理的准确性要求，选择消费进度自动提交或手动提交，在异常处理设计较为复杂时，推荐使用手动控制消费位点提交。
消费者应配置负载均衡，确保消息在多个消费者之间均匀分配。
消费者应评估消费速率，避免消息过多导致应用崩溃，以及消息并发过低导致消息堆积。
消息堆积设计
设计消息系统时，应评估生产者与消费者的生产速率，在流量高峰场景下确保生产者、消费者性能，确保消息服务缓冲区可承载峰值流量，推荐设计消费者动态扩容方案，可参考以下设计。
提升消费速率：消费者并发度应与消息服务资源匹配，消费者数量应与消费者主题队列数匹配，消费者推荐使用多线程消费、异步处理等设计保障消费者消费性能。
支持消费者扩容：应将消费者设计为无状态服务，并根据峰值流量预留消费者扩容资源。
消息拓扑设计
接入系统在设计阶段应统筹评估消息系统拓扑关系，如存在跨系统消息交互，还应在拓扑关系中标识关联系统的主题、生产者、消费者，并根据业务场景评估生产者数量、消费者数量、消息体大小、并发度、消息标签等方面的设计。
某系统群消息拓扑设计示例，具体请见表6。

表6  某系统群消息拓扑设计表
容错设计
接入系统应根据系统等级、可用性要求、灾难恢复要求，明确对消息服务的依赖程度，在设计消息相关接口调用时应评估容错机制，以提升系统稳定性，可参考以下设计。
健康检查：设计健康检查接口，包含消息生产、消费结果是否正常，并补充监控、告警指标。
服务熔断：合理配置超时时间、失败重试次数，当访问消息服务异常时熔断请求，避免应用线程hang死，导致故障范围扩散。
服务降级：当消息生产异常时接口降级，设计核心交易时，确保消息发送不影响主流程业务。
错误处理：合理捕获异常，并设计错误处理方案，记录关键错误日志。
请求重试：重要消息接口设计业务重试方案，在网络抖动时可捕获特定异常进行重试。
容灾设计
方案选型
接入系统在建设单元化/双多活能力时，应结合系统架构设计选择使用消息服务高阶能力，高阶能力在实际落地中可组合使用。
热备模式：消息服务同城机房单向同步，应用访问主机房服务。接入系统读写数据均访问主机房，仅在容灾切换后访问同城容灾机房，消息同步早于消费位点，容灾切换需处理重复消费。
独立服务：消息服务机房独立部署，应用访问本地机房服务。接入系统读写数据均访问本地机房，消息无灾备，无法跨机房传输消息。
单元化模式：消息服务同城/异地机房双向同步单元化消息，应用访问本地机房服务。接入系统读写数据均访问本地机房，生产者生产消息本单元无消费者将同步至对应单元，由对应单元消费者消费。
消息路由模式：消息服务同城/异地机房双向同步全量消息，应用访问本地机房服务。
功能选型
接入系统明确设计方案后，应选择消息同步方案和容灾切换方案。
消息同步：
单向同步：主机房同步消息、位点至同城容灾机房，容灾切换后需通过运维处置反转同步关系。
双向同步单元化消息：主机房、同城/异地容灾机房消息双向同步，不同步位点信息，跨单元消息将同步至对应单元机房，消费者获取单元化路由信息后处理消息。
双写同步全量消息：主机房、同城/异地容灾机房消息双向同步，不同步位点信息，全量消息同步至容灾机房。
容灾切换：消息服务目前提供消息同步功能，依赖应用侧客户端设计实现容灾切换，目前提供DNS域名切换和配置中心全局地址切换两种方案。
功能限制
接入系统使用消息服务容灾功能时，应明确消息服务功能限制，具体限制如下。
重复消费：热备模式、单元化模式、消息路由模式均无法确保消费者仅消费一次消息，消费者根据本地机房消费位点处理重复消息后完成消费，应用侧应设计消费去重逻辑。
同步关系反转：热备模式下在容灾切换后，需手动反转消息同步关系。
依赖组件：依赖配置中心组件和JUP平台GLS组件。
开发指引
接入系统在编码阶段应规范化消息服务使用，包括服务端、客户端版本以及相关配置，应遵循开发规范。
服务端版本要求
应符合附录A相关文件要求的消息服务版本。
客户端版本要求
消息服务支持JAVA客户端，因开源软件持续保持更新，客户端具体版本选择时应根据最新开源技术目录，具体见表7。



表7  客户端版本说明
客户端配置
生产者配置参数
接入系统设计生产者时应评估客户端参数配置，下述为4.X客户端相关参数的配置建议，应结合系统设计、测试等实际情况配置连接池、超时等待等参数，具体见表8。
表8  4.X生产者配置参数说明
消费者配置参数
接入系统设计生产者时应评估客户端参数配置，下述为4.X客户端相关参数的配置建议，应结合系统设计、测试等实际情况配置连接池、超时等待等参数，具体见表9。
表9  4.X消费者配置参数说明

生产者开发说明
接入系统开发生产者应用时，应结合业务特性开发相关代码，包括异步初始化、日志记录、请求重试等。
生产者初始化
生产者初始化异常不能影响应用启动的主流程，建议采用异步进程初始化生产者。
生产者应避免频繁创建、销毁连接，生产者底层会统一维护连接池，初始化完成后将创建长连接提供生产者使用。
接入系统应避免在单一进程中创建大量生产者实例，单个生产者可向多个主题发送消息，推荐最大化复用生产者对象。
生产者创建伪代码

消息标签、消息健使用
生产者推荐使用Tag和Key细粒度划分消息，可通过Tag标识消息子类型、业务场景，通过Key为消息配置业务标识符，可在消息索引、消息查询和消息去重等常见使用。
生产者根据业务标识消息Tag和消息Key伪代码

生产者日志记录
生产者应记录消息发送日志，用于排查消息链路传输异常等问题，建议记录为Info级别，并根据本行日志规范，对敏感业务数据进行脱敏处理，日志记录范围包括但不限于消息发送、消息重试接口。
重连重试
生产者应配置重试次数、重试间隔参数，确保消息发送时的异常网络波动（生产者默认支持重连重试配置）。
消息非易失场景下，接入系统应设计业务侧故障处置策略，推荐在发送消息失败时将消息写入持久化存储或DB，通过业务重试或业务补偿保证消息发送不丢失。
生产者同步发送消息重试伪代码
生产者异步发送消息重试伪代码
SpringBoot接入生产者同步发送消息重试伪代码
SpringBoot接入生产者异步发送消息重试伪代码

事务消息
生产者使用事务消息时，推荐自定义事务监听器，并重写executeLocalTransation方法和checkLocalTransaction方法，并评估事务消息引入的时延和性能损耗，确保接口设计满足业务时效性要求。
生产者事务消息初始化伪代码
顺序消息
生产者发送顺序消息时，应根据消息顺序性要求，选择消息全局顺序或消息分区顺序（全局顺序模式下，服务端应配置主题队列数为1，此时该队列并发度为1）；
接入系统选择分区顺序模式时，应根据业务数据唯一标识，重写队列选择方法，推荐根据业务标识分配消息所属队列。
生产者配置顺序消息分布伪代码
Springboot接入生产者配置顺序消息分布伪代码
延时消息
生产者发送延时消息时，应明确延时发送时间，并配置消息的延时级别参数，默认情况下消息服务延时级别为1到18级，分别表示延时发送时间为1s、5s、10s、30s、1m、2m、3m、4m、5m、6m、7m、8m、9m、10m、20m、30m、1h。
生产者如需使用延时级别外的延时时间，可在服务端调整延时级别代表的延时时间，接入系统应在申请消息服务时说明上述需求。
生产者配置延时级别参数伪代码
SpringBoot生产者配置延时级别参数伪代码

消费者开发说明
接入系统开发消费者应用时，应结合业务特性开发相关代码，包括异步初始化、日志记录、消费幂等处理等。
消费者初始化
消费者启动时应正确配置消费者组、订阅主题、标签，并根据消息类型选择消息监听器，推荐使用异步方式启动消费者，避免应用启动时消费者异常影响应用启动。
消费者初始化伪代码
SpringBoot接入消费者初始化伪代码
消息幂等处理
消息服务提供的消费功能为至少投递一次（at least once），在精准消费（exactly once）场景下，消费者应用设计时应设计业务测消息去重处理，保障消费幂等性，推荐使用关系型数据库进行去重，消息服务仅用于异步通知。
消费者消息幂等处理伪代码
消费者日志记录
消费者应记录消息处理日志，用于排查消息链路传输异常等问题，建议记录为Info级别，并根据本行日志规范，对敏感业务数据进行脱敏处理，日志记录范围包括但不限于消息接收、消息处理、消息去重、消息重试接口。
消费重试
消费者应配置消费重试次数参数，确保消息消费时网络波动导致消费提交失败（消费者默认支持消费重试配置，确保消息处理业务逻辑具备容错性）。
消息非易失场景下，接入系统应设计业务侧消息重试，推荐通过重试队列和异步进程处理消费失败的消息。
消费者设计同步重试接口，应控制重试次数，并确保消费时间不超过最大消费时间限制。
顺序消费
消费者顺序消费时，推荐配置顺序消费监听器，并使用同步逻辑处理消息，避免消息乱序，同时在消费重试、错误处理过程中评估重试次数、超时时间并设计异常处置方案，避免消费阻塞。
死信队列
推荐使用死信队列统一处理未消费成功的消息，不同消费者组可使用不同死信队列主题（%DLQ%ConsumerGroup为死信队列主题），同时死信消息消费处理逻辑应与普通消息保持一致。
安全编码
接入系统接入消息服务时，应结合系统安全要求设计，遵循相关的安全原则。
服务认证：应开启客户端认证，根据密码规范配置接入密码。
数据加密：业务数据应加密后再通过消息服务传输，并满足我行数据安全要求。
权限隔离：根据最小必须原则分配消费者组、生产者组的主题读写权限。
测试指引
接入系统在测试阶段，应规范化消息服务相关接口测试过程，按照测试要求进行功能及性能测试，建议增加专项测试，以验证在某些故障场景下系统的应对能力，确保符合接入系统的功能要求和可用性要求。
性能测试
接入系统测试消息相关接口性能时，应使用全链路性能测试，提前评估消息容量、TPS，重点设计消息堆积、生产消费速率匹配等性能测试案例，确保接口符合性能要求。
专项测试
接入系统应评估消息服务的异常切换、宕机影响，建议在专项测试中重点评估以下场景对接入系统的影响，明确接入系统在故障过程中、故障恢复后的业务影响，可参考以下专项测试案例。
表11  专项测试案例说明
可参考上述案例，根据接入系统可用性要求补充混沌案例进行专项测试。
上线指引
接入系统在上线阶段，应从系统维度准备生产下发方案并识别风险，结合技术中台相关服务接入指引和运维单位要求，完成上线前置准备、下发检查、告警规则调整和应急卡片编写等工作。
前置资源准备
接入系统如需在生产环境接入消息服务，可通过IT综合管理系统发起软件维护需求，在施工完成后，将反馈回执信息至申请单位。
在申请软件维护需求时，应在流程附件中提供系统概要设计说明书并明确服务资源需求，应重点关注：接入区域、服务部署模式、资源需求、持久化模式和容灾要求，以及主题、生产者组、消费者组、权限需求，并根据本文设计指引确定是否存在定制化需求，如顺序消息、主题队列数、延时级别等，也需在流程附件中说明。
告警规则确认
消息服务默认接入技术中台可观测底座，提供标准化的监控、日志、告警能力。接入系统可根据业务本文设计指引，评估服务默认模板的监控项、告警阈值是否满足需求，并根据业务特点调整监控项和告警项，研发测试环境验证通过后提交至生产应用运维人员更新生产环境监控指标及告警规则。
接入前置检查
接入系统在上线或首次接入消息服务时，应完成系统投产及维护下发前的检查核对工作，包括客户端配置确认、生产服务检查等，并根据消息服务回执单，并联系生产应用运维人员完成生产资源接入前检查，包括服务部署模式确认、生产资源确认、网络连通性确认、连接认证确认等，并确认主题、消费者组、权限信息无误，确保接入系统客户端配置信息准确无误。
应急卡片准备
接入系统在上线或首次接入消息服务时，应结合消息服务使用情况完成接入系统的应急预案（卡片）编写，应重点编写消息堆积场景下消费者扩容应急预案，并提交至生产应用运维人员。

（规范性）
指导文件
A.1行内指导文件
本文件应符合行内指导文件要求，包括但不限于：
兴业银行，《兴业银行技术平台目录》；
兴业银行，《兴业银行软件技术平台版本序列及兼容列表》。
未注明发文号的，应遵照最新版本。
_________________________________


|  |
| --- |


| 模式 | 说明 |
| --- | --- |
| 单点模式 | 该模式无高可用能力，集群中只有一个节点，宕机后不可用 |
| 主从模式 | 该模式提供数据高可用，集群包含多个Broker主、从节点，主节点宕机后，可手动将从节点设置为新的主节点 |
| Dleger高可用模式 | 该模式在主从模式的基础上，增加主从节点故障自动切换的能力，实现服务的高可用。基于DLedger组件实现Broker主从节点故障自动转移，并确保数据在主从节点之间成功同步 |


| 消息落盘模式 | 说明 |
| --- | --- |
| 异步刷盘模式（默认模式） | 该模式下Broker在写入消息到二进制文件时，会先将消息写入OS的内存页（PageCache），再在通过后台线程写入磁盘，在极端场景下生产者发送消息成功，内存页数据可能还未写入磁盘时，如发生服务宕机可能出现消息丢失 |
| 同步刷盘模式 | 该模式下生产者发送消息后，服务端会在消息落盘后再返回请求，可确保消息生产不丢失 |


| 消息复制模式 | 说明 |
| --- | --- |
| 同步复制 | 该模式下生产者发送消息时，Broker主从节点都写成功，才返回成功，brokerRole配置为SYNC_MASTER |
| 异步复制 | 该模式下生产者发送消息时，Broker主节点写成功就返回成功，brokerRole配置为ASYNC_MASTER |
| DLedger复制 | 该模式下生产者发送消息时，Broker主节点写成功，并要求至少消息复制到50%以上的节点之后，才返回成功，brokerRole配置为SYNC_MASTER |


| 磁盘使用率 | 消息过期清理说明 |
| --- | --- |
| 磁盘使用率低于75% | 定时（每日凌晨4点）清理过期的消息文件 |
| 磁盘使用率达到75% | 未达到每日清理时间，触发清理过期的消息文件 |
| 磁盘使用率达到85% | 无论文件是否过期，触发清理时间最早的消息文件 |
| 磁盘使用率达到90% | 拒绝消息写入，触发清理时间最早的消息文件，直到磁盘使用率降低90% |


| 消息类型 | 说明 |
| --- | --- |
| 普通消息 | RocketMQ提供的基础消息类型，无其余特性，常用于应用对消息处理时间、处理顺序没有额外要求的场景 |
| 延迟消息 | RocketMQ提供的一种高级消息类型，消息被发送至服务端后，在指定时间后才能被消费者消费 |
| 顺序消息 | RocketMQ提供的一种高级消息类型，支持消费者按照发送消息的先后顺序获取消息，从而实现业务场景中的顺序处理 |
| 事务消息 | RocketMQ提供的一种高级消息类型，支持在分布式场景下保障消息生产和本地事务的最终一致性 |


| 系统名称 | 主题名称 | 消息体大小 | TPS | 生产者组 | 消费者组 |
| --- | --- | --- | --- | --- | --- |
| j037x0 | j037x0_user | 1K | 10 | pg_j037x0_controller（2个实例） | / |
| j037x0 | j037x0_order_created | 1K | 200 | pg_j037x0_payment（5个实例） | / |
| j037x0 | j037x0_order_status | 1K | 200 | pg_j037x0_payment（5个实例） | / |
| j037x0 | j037x0_inventory | 1K | 200 | pg_j037x0_payment（5个实例） | / |
| j037x0 | j037x0_order_payment | 2K | 200 | pg_j037x0_payment（5个实例） | / |
| j036x0 | j037x0_user | 1K | / | / | cg_j036x0_platform（2个实例） |
| j036x0 | j037x0_order_created | 1K | / | / | cg_j036x0_order（5个实例） |
| j036x0 | j037x0_order_status | 1K | / | / | cg_j036x0_order（5个实例） |
| j036x0 | j037x0_inventory | 1K | / | / | cg_j036x0_inventory（2个实例） |
| j035x0 | j037x0_order_payment | 2K | / | / | cg_j035x0_payment（2个实例） |
| j035x0 | j037x0_order_status | 1K | / | / | cg_j035x0_order（5个实例） |


| 客户端类型 | 版本要求 | 是否纳入开源技术目录 | 说明 |
| --- | --- | --- | --- |
| rocketmq-client | ≥4.9.6 | 是 | 4.X版本客户端在使用RocketMQ 4.X版本消息服务服务端使用
5.0及以上客户端为Grpc协议，在使用RocketMQ 5.X版本消息服务服务端使用 |


| 配置参数 | 配置说明 | 默认配置 | 配置要点 |
| --- | --- | --- | --- |
| producerGroup | 生产者组 | DEFAULT_PRODUCER | 禁止使用模式值，按照规范配置为生产者组名称 |
| nameSrvAddr | 集群连接地址 | 无 | 1.配置多个NameServer地址，使用分号分隔
2.禁止配置为HttpSite地址 |
| aclClientRpcHook | ACL认证信息 | 无 | 配置为消息服务的AK/SK |
| maxMessageSize | 消息体最大限制 | 4MB | 1.无特殊需求使用默认值
2.如需调整需要根据性能测试结果确认并同步调整服务端消息体限制 |
| defaultTopicQueueNums | 默认主题队列数 | 4 | 禁止配置，不允许配置自动创建主题 |
| compressMsgBodyOverHowmuch | 消息压缩阈值 | 4096 | 1.无特殊需求使用默认值
2.如需调整需要根据性能测试结果确认 |
| sendMsgTimeout | 消息发送超时时间 | 3000 | 1.无特殊需求使用默认值
2.根据生产者重试要求及性能测试结果确认配置 |
| retryTimesWhenSendFailed | 同步发送消息失败重试次数 | 2 | 1.根据生产者重试设计进行配置
2.根据生产者重试要求及性能测试结果确认配置 |
| retryTimesWhenAsyncSendFailed | 异步发送失败消息重试次数 | 2 | 1.根据生产者重试设计进行配置
2.根据生产者重试要求及性能测试结果确认配置 |
| SendLatencyFaultEnable | 消息发送规避故障Broker节点 | False | 无特殊需求使用调整为True |
| retryAnotherBrokerWhenNotStoreOK | 消息发送重试至其余Broker | False | 1.使用异步发送时，使用默认值
2.使用同步发送时，调整配置参数为True |
| createTopicKey | 自动创建Topic的默认Key | TBW102 | 禁止配置，不允许自动创建不存在的Topic |


| 配置参数 | 配置说明 | 默认配置 | 配置要点 |
| --- | --- | --- | --- |
| consumerGroup | 消费者组 | Default_group | 禁止使用模式值，按照规范配置为生产者组名称 |
| nameSrvAddr | 集群连接地址 | 无 | 1.配置多个NameServer地址，使用分号分隔
2.禁止配置为HttpSite地址 |
| aclClientRpcHook | ACL认证信息 | 无 | 配置为消息服务的AK/SK |
| subscription | 订阅主题信息和Tag | 无 | 配置为消费者的订阅主题及消息标签，仅在主题和消息标签匹配的消息才会被消费 |
| messageListener | 订阅主题的消息监听处理器 | 无 | 根据消息类型选择监听器类型并实现消费逻辑：MessageListennerConcurrently（非顺序消费）、MessageListennerOrderly（顺序消费） |
| messageModel | 消费模式 | Clustering | 根据消费者设计选择Clustering（集群消费）或Broadcasting（广播消费） |
| consumeFromWhere | 消费者实例开始消费偏移点 | CONSUME_FROM_LAST_OFFSET | 根据消费者业务逻辑确认配置：CONSUME_FROM_LAST_OFFSET（从最后一条消息下一位开始消费，如果生产者早于消费者上线，此种模式会不会消费启动前的消息）、CONSUME_FROM_FIRST_OFFSET（初次接入从消息队列头部消费，后续启动根据上次的消费进度）、CONSUME_FROM_TIMESTAMP（从指定时间时间点开始消费） |
| maxReconsumeTime | 消息最大重试次数，-1表示重试16次 | -1 | 1.无特殊需求使用默认值，达到最大重试次数后消息将进入死信队列
2.根据消费者重试要求及性能测试结果确认配置 |
| consumeTimestamp | 消费者开始消费的指定时间点，不配置默认为30分钟前，配置参数需按照时间字符串格式 | YyyyMMddHHmmss | 1.根据业务需求调整消费开始时间
2.该参数仅在消费偏移点设置为CONSUME_FROM_TIMESTAMP时生效 |
| consumeTimeout | 消费者最大超时时间，单位分钟 | 15 | 1.根据业务重试策略配置超时，如消费重试时效性无特殊需求使用默认值
2.消费时效性要求较高时，可调整该参数，根据性能测试结果确认配置 |
| consumeThreadMin | 消费者最小线程数 | 20 | 1.无特殊需求使用默认值
2.根据消费者并发要求及性能测试结果确认配置 |
| consumeThreadMax | 消费者最大线程数 | 20 | 1.无特殊需求使用默认值
2.根据消费者并发要求及性能测试结果确认配置 |
| pullBatchSize | 拉取消费模式下单次拉取消息至客户端的消息数量 | 32 | 1.无特殊需求使用默认值
2.根据消费者并发要求及性能测试结果确认配置 |
| pullInterval | 消费者拉取消息间隔时间，单位毫秒 | 0 | 无特殊需求使用默认值 |
| pullThresholdForQueue | 拉取消息本地最大缓存消息数 | 1000 | 1.无特殊需求使用默认值
2.根据消费者并发要求及性能测试结果确认配置 |
| consumeConcurrentlyMaxSpan | 并发消费单个线程同时处理的消息队列跨度 | 2000 | 1.无特殊需求使用默认值
2.根据消费者并发要求及性能测试结果确认配置 |
| consumeMessageBatchMaxSize | 单次拉取消息并处理的消息数量 | 1 | 1.无特殊需求使用默认值
2.如需开启批量消费，可调整该参数，根据并发要求及性能测试结果确认配置 |
| offsetStore | 位点存储模式 | 根据消费模式自动配置 | 禁止配置，根据消费模式自动配置 |
| pullThresholdSizeForQueue | 单个队列可拉取的消息字节总量，单位MB，超过该阈值将触发流量控制，消费者将延迟拉取消息，该参数值需在1到1024之间 | 100 | 1.无特殊需求使用默认值
2.如消息数量较多且存在峰值流量，可调整该参数，根据并发要求及性能测试结果确认配置
3.该参数调大会占用较多内存，可能出现内存溢出 |
| pullThresholdForQueue | 单个队列可拉取的消息数量，超过该阈值将触发流量控制，消费者将延迟拉取消息，该参数值需在1到65535之间 | 1000 | 1.无特殊需求使用默认值
2.如消息数量较多且存在峰值流量，可调整该参数，根据并发要求及性能测试结果确认配置
3.该参数调大会占用较多内存，可能出现内存溢出 |
| pullThresholdSizeForTopic | 单个主题最大缓存消息字节总量，单位MB，-1标识不限制 | -1 | 1.无特殊需求使用默认值，通过单个队列进行限制
2.该配置项优先级低于pullThresholdForQueue参数配置 |
| pullThresholdForTopic | 单个主题最大缓存消息数，-1表示不限制 | -1 | 1.无特殊需求使用默认值，通过单个队列进行限制
2.该配置项优先级低于pullThresholdForQueue参数配置 |
| suspendCurrentQueueTimeMillis | 消费者流量控制，暂停拉取消息的时间，单位毫秒 | 1000 | 无特殊需求使用默认值 |


| /**
* 示例：生产者创建伪代码，仅供参考，如需使用请经过测试验证
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 类描述：RocketMQ生产者类
* 说明：根据生产者应用框架调整，使用springboot框架还需评估服务注册
*/
public class RocketMQProducer {
    public void initializeProducerAsync() {
// 配置NameServer地址，ACL认证
String aclToken = decodeSMS4Token("{SMS4}adncogk52==");
producer = new DefaultMQProducer("please_rename_unique_group_name", new AclClientRPCHook(new SessionCredentials("RocketMQ",aclToken)));
producer.setNamesrvAddr("name-server1-ip:9876;name-server2-ip:9876");
// 配置超时时间、同步重试次数
producer.setSendMsgTimeout(6000);
producer.setRetryTimesWhenSendFailed(6);
// 异步启动Producer，不影响应用系统启动
ExecutorService executorService = Executors.newSingleThreadExecutor();
executorService.submit(() -> {
int attempts = 0;
while (attempts < maxRetryAttempts) {
try {
producer.start();
break; 
} catch (MQClientException e) {
attempts++;
// 打印初始化生产者重试日志
if (attempts < maxRetryAttempts) {
try {
TimeUnit.MILLISECONDS.sleep(retryDelay);
} catch (InterruptedException interruptedException) {
Thread.currentThread().interrupt();
}
}
}
}
    }
} |
| --- |


| /**
* 示例：生产者根据业务标识消息Tag和消息Key伪代码，仅供参考
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：发送消息，并根据设置业务标识Tag和Key
* @param message 发送的消息字符串数据
* @return
* @throw MQException 抛出消息发送异常
*/
public void sendMessage(String msg) throws MQException {
try{
Message msg = new Message(
"Topic",  // 发送消息的主题
"Tag",   // 发送消息的Tag标识，可用来区分消息子类型
"Business Key", //发送消息的Key标识，可用来标识唯一性
msg.getBytes(RemotingHelper.DEFAULT_CHARSET)
);
this.producer.send(msg);
} catch (Exception e) {
//处理消息发送异常
}
} |
| --- |


| /**
* 示例：生产者同步发送消息重试伪代码，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：同步发送消息，并增加重试机制
* @param producer RocketMQ 生产者实例
* @param message 需要发送的消息
* @param retryTimes 最大业务重试次数
* @param retryDelayMs 每次重试之间的等待时间（毫秒）
* @return SendResult 发送信息结果
* @throw MQException 抛出消息发送异常
*/
public SendResult sendMessageWithRetry(DefaultMQProducer producer, Message message, int retryTimes, long retryDelayMs) throws Exception {
int attempt = 0;
while (attempt < retryTimes) {
            try {
                SendResult sendResult = producer.send(message);
                // 消息发送日志打印
                return sendResult; // 成功则返回发送结果
            } catch (MQClientException | RemotingException | MQBrokerException | InterruptedException e) {
                attempt++;
                // 消息发送重试日志打印
                if (attempt < retryTimes) {
                    try {
                         Thread.sleep(retryDelayMs);
                    } catch (InterruptedException interruptedException) {
                        Thread.currentThread().interrupt();
                        throw interruptedException; 
                    }
                } else {
                    // 消息发送失败异常日志打印，并根据业务需求将消息落盘或落库
                    throw e; 
                }
            }
        }
// 防御式编程
        throw new Exception("Message sending failed after all retry attempts."); 
    } |
| --- |


| /**
* 示例：生产者异步发送消息重试伪代码，仅供参考
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 类描述：RocketMQ生产者异步发送类
* 说明：根据生产者应用框架调整，使用springboot框架还需设计服务注册
*/
public class RocketMQAsyncProducer {
    private final DefaultMQProducer producer;
    private final int retryTimes;
    private final long retryDelayMs;
    public RocketMQAsyncProducer(DefaultMQProducer producer, int retryTimes, long retryDelayMs) {
        this.producer = producer;
        this.retryTimes = retryTimes;
        this.retryDelayMs = retryDelayMs;
    }

    /**
     * 异步发送消息，带有业务重试机制
     * @param message 需要发送的消息
     * @return
     */
    public void sendMessageWithRetry(Message message) {
        sendMessageWithRetryInternal(message, 0);
    }

    /**
     * 内部方法，用于实现重试机制
     * @param message 需要发送的消息
     * @param attempt 当前重试次数
     * @return
     */
    private void sendMessageWithRetryInternal(Message message, int attempt) {
        producer.send(message, new SendCallback() {
            @Override
            public void onSuccess(SendResult sendResult) {
                // 消息发送成功日志打印
            }
            @Override
            public void onException(Throwable e) {
                int nextAttempt = attempt + 1;
                if (nextAttempt < retryTimes) {
                    try {
                        Thread.sleep(retryDelayMs);
                        // 消息发送重试日志打印
                        sendMessageWithRetryInternal(message, nextAttempt);
                    } catch (InterruptedException interruptedException) {
                        Thread.currentThread().interrupt();
                    }
                } else {
                    // 消息发送失败日志打印，并根据业务需求将消息落盘或落库
                }
            }
        });
    }
} |
| --- |


| /**
* 示例：生产者同步发送消息重试伪代码，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：同步发送消息并增加重试机制，根据rocketmq-client客户端版本要求选择匹配的
* RocketMQStarter版本和SpringBoot版本。
* @param Topic RocketMQ topic
* @param message 需要发送的消息
* @param retryTimes 最大业务重试次数
* @param retryDelayMs 每次重试之间的等待时间（毫秒）
* @throw MQException 抛出消息发送异常
*/
@Autowired
private RocketMQTemplate rocketMQTemplate;


public void sendMessageWithRetry(String Topic, String message, int retryTimes, long retryDelayMs) throws Exception {
int attempt = 0;
while (attempt < retryTimes) {
            try {
                rocketMQTemplate.send(Topic, MessageBuilder.withPayload(message).build());
            } catch (MessagingException e) {
                attempt++;
                // 消息发送重试日志打印
                if (attempt < retryTimes) {
                    try {
                         Thread.sleep(retryDelayMs);
                    } catch (InterruptedException interruptedException) {
                        Thread.currentThread().interrupt();
                        throw interruptedException; 
                    }
                } else {
                    // 消息发送失败异常日志打印，并根据业务需求将消息落盘或落库
                    throw e; 
                }
            }
        }
// 防御式编程
        throw new Exception("Message sending failed after all retry attempts."); 
    } |
| --- |


| /**
* 示例：生产者异步发送消息重试伪代码，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：异步发送消息并增加重试机制，根据rocketmq-client客户端版本要求选择匹配的
* RocketMQStarter版本和SpringBoot版本。
* @param Topic RocketMQ topic
* @param message 需要发送的消息
* @param retryTimes 最大业务重试次数
* @throw MQException 抛出消息发送异常
*/
@Autowired
private RocketMQTemplate rocketMQTemplate;

public void sendMessageWithRetry(String Topic, String message, int retryTimes) throws Exception {
rocketMQTemplate.asyncSend(Topic, MessageBuilder.withPayload(message).build(), new SendCallback() {
           @Override
           public void onSuccess(SendResult sendResult) {
                 // 消息发送成功日志打印
           }

           @Override
           public void onException(Throwable throwable) {
              int nextAttempt = attempt + 1;
                if (nextAttempt < retryTimes) {
                    try {
                        Thread.sleep(retryDelayMs);
                        // 消息发送重试日志打印
                       sendMessageWithRetry(Topic, message, retryTimes) 
} catch (InterruptedException interruptedException) {
                        Thread.currentThread().interrupt();
                    }
                } else {
                    // 消息发送失败日志打印，并根据业务需求将消息落盘或落库
                }
           }
       });
    } |
| --- |


| /**
* 示例：生产者事务消息初始化伪代码，仅供参考
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：RocketMQ初始化事务消息生产者方法
* 说明：本方法仅描述设置事务监听器部分代码逻辑，无法直接使用
*/
public void initTransactionProducer {
        // 设置事务监听器
        producer.setTransactionListener(new TransactionListener() {
            @Override
            public LocalTransactionExecutor executeLocalTransaction(Message msg, Object arg) {
                try {
// 本地事务执行逻辑
// 根据事务执行结果返回 COMMIT_MESSAGE、ROLLBACK_MESSAGE 或 UNKNOWN
                    if (localTransactionSuccess) {
                        return LocalTransactionExecutor.COMMIT_MESSAGE;
                    } else {
                        return LocalTransactionExecutor.ROLLBACK_MESSAGE;
                    }
                } catch (Exception e) {
                    return LocalTransactionExecutor.UNKNOWN;
                }
            }

            @Override
            public TransactionResolutionStatus checkLocalTransaction(MessageExt msg) {
                // 本地事务状态检查逻辑
                // 返回 COMMIT_TRANSACTION、ROLLBACK_TRANSACTION 或 UNKNOWN
                return TransactionResolutionStatus.COMMIT_TRANSACTION;
            }
        });
} |
| --- |


| /**
* 示例：生产者配置顺序消息分布伪代码，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：配置顺序消息所属队列，并发送顺序消息
* 说明：本方法仅描述配置顺序消息所属队列部分代码逻辑，无法直接使用
* @param message 需要发送的消息
* @param orderId  需要确保顺序的ID
* @return 
* @throw MQException  抛出消息发送异常
*/
public void sendOrderMessage(String msg,long orderId) throws MQException {
Message message = new Message("test", "TagA", msg.getBytes(RemotingHelper.DEFAULT_CHARSET));
// orderId为业务侧需要确保顺序的标识
SendResult sendResult = producer.send(message, new MessageQueueSelector() {
          @Override
          public MessageQueue select(List<MessageQueue> mqs, Message msg, Object arg) {
                // 分区顺序消息时根据业务唯一标识分配队列
                Integer id = (Integer) arg;
                int index = id % mqs.size();
                return mqs.get(index);
                // 全局顺序消息时直接返回0号队列
                // return mqs.get(0);
          }
}, orderId);
} |
| --- |


| /**
* 示例：生产者配置顺序消息分布伪代码，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：配置顺序消息所属队列，并发送顺序消息，根据rocketmq-client客户端版本要求* 选择匹配的RocketMQStarter版本和SpringBoot版本。
* 说明：本方法仅描述配置顺序消息所属队列部分代码逻辑，无法直接使用
* @param message 需要发送的消息
* @param orderId 需要确保顺序的key
* @return 
* @throw MQException 抛出消息发送异常
*/
@Autowired
private RocketMQTemplate rocketMQTemplate;

public void sendOrderMessage(String topic,String msg,String orderId) throws MQException {
// orderId为业务侧需要确保顺序的标识
rocketMQTemplate.sendOrderly(topic, MessageBuilder.withPayload(msg).build(), orderId);
} |
| --- |


| /**
* 示例：生产者配置延时级别，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：设置延时消息级别，并发送延时消息
* 说明：本方法仅描述配置延时消息级别代码逻辑，无法直接使用
* @param message 需要发送的消息
* @param level 延时级别
* @return 
* @throw MQException  抛出消息发送异常
*/
public void sendDelayMessage(String msg,int level) throws MQException {
    try{
        Message message = new Message("test", "TagA", msg.getBytes(RemotingHelper.DEFAULT_CHARSET));
        //根据业务延时时间需求确定延迟级别
        message.setDelayTimeLevel(level);     
        SendResult sendResult = producer.send(message); 
      } catch (Exception e) {
        //处理消息发送异常
}
} |
| --- |


| /**
* 示例：生产者配置延时级别，仅供参考 
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 方法描述：设置延时消息级别，并发送延时消息，根据rocketmq-client客户端版本要求
* 选择匹配的RocketMQStarter版本和SpringBoot版本。
* 说明：本方法仅描述配置延时消息级别代码逻辑，无法直接使用
* @param topic RocketMQ topic
* @param message 需要发送的消息
* @param level 延时级别
* @return 
* @throw MQException  抛出消息发送异常
*/
@Autowired
private RocketMQTemplate rocketMQTemplate;

public void sendDelayMessage(String topic,String msg,int level) throws MQException {
    try{
rocketMQTemplate.sendOrderly(topic, MessageBuilder.withPayload(msg).setHeader(MessageConst.PROPERTY_DELEY_TIME_LEVEL,level).build());
      } catch (Exception e) {
        //处理消息发送异常
}
} |
| --- |


| /**
* 示例：消费者初始化伪代码，仅供参考  
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 类描述：RocketMQ消费者类
* 说明：根据消费者应用框架调整，使用springboot框架还需设计服务注册
*/
public class RocketMQConsumer {
    private String consumerGroup;
    private String namesrvAddr;
    private String topic;
    private DefaultMQPushConsumer consumer;

    public RocketMQConsumer(String consumerGroup, String namesrvAddr, String topic) {
        this.consumerGroup = consumerGroup;
        this.namesrvAddr = namesrvAddr;
        this.topic = topic;
    }

    public void start() {
        consumer = new DefaultMQPushConsumer(consumerGroup);
        consumer.setNamesrvAddr(namesrvAddr);
      // 根据业务场景确认位点消费逻辑、消费类型
        consumer.setConsumeFromWhere(ConsumeFromWhere.CONSUME_FROM_FIRST_OFFSET);
        consumer.setMessageModel(MessageModel.CLUSTERING);

        try {
            // 根据业务场景确认订阅主题和标签
            consumer.subscribe(topic, "*");
            // 根据业务场景选择注册消息监听器类型
            consumer.registerMessageListener(new MessageListenerConcurrently() {
            @Override
            public ConsumeConcurrentlyStatus consumeMessage(List<MessageExt> msgs,
                                                                ConsumeConcurrentlyContext context) {
                    // 消息处理逻辑
                    return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
              }
            });
            // 启动消费者实例
            consumer.start();
        } catch (MQClientException e) {
            // 打印异常信息但不抛出异常，以保证应用正常启动
        }
    }

    public void shutdown() {
        if (consumer != null) {
            consumer.shutdown();
        }
    }
} |
| --- |


| /**
* 示例：消费者初始化伪代码，仅供参考  
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 类描述：RocketMQ消费者类，根据rocketmq-client客户端版本要求选择匹配的
* RocketMQStarter版本和SpringBoot版本。
*/
@Service
@RocketMQMessageListener(topic = "test-topic-1", consumerGroup = "my-consumer_test-topic-1")
public class MyConsumer1 implements RocketMQListener<String>{
    public void onMessage(String message) {
            // 消息处理逻辑
        }
} |
| --- |


| /**
* 示例：消费者幂等处理伪代码，仅供参考  
* @author 技术中台服务岗
* @version 1.0 2024-8-1
* 代码块描述：RocketMQ消费者注册监听器自定义consumeMessage方法通过Key进行去重
* 说明：本方法仅描述消费者判断消息是否重复部分代码逻辑，无法直接使用
*/
consumer.registerMessageListener(new MessageListenerConcurrently() {
@Override
public ConsumeConcurrentlyStatus consumeMessage(List<MessageExt> msgs,                                                       ConsumeConcurrentlyContext context) {
       try {
         for (MessageExt msg: msgs) {
            // 使用消息Key作为业务标识
            String uniqueID = msg.getKeys();
            // 消息根据uniqueID进行去重判断，如已经消费则跳过该消息
            if (businessMessageDeduplication(uniqueID)) {
                continue;
} 
// 消息处理业务逻辑，根据业务需求选择同步或者异步方案
}
return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
       }catch (Exception e) {
 		    //主动捕获异常相关异常，重要的消息需要主动重试消费
         return ConsumeConcurrentlyStatus.RECONSUME_LATER;
       }
}
}); |
| --- |


| 专项测试案例 | 测试说明 |
| --- | --- |
| RocketMQ（应用端）网络抖动演练 | 本场景模拟应用端到RocketMQ网络抖动导致通信异常出现消息丢失场景，验证应用是否具备消息生产重试的能力，是否具备消息补偿能力。 |
| RocketMQ极端场景Broker全量宕机场景 | 本场景模拟RocketMQ服务因故障全部宕机场景，验证接入系统是否在应用故障处置后，是否具备自动重连能力，消息生产和消费逻辑是否正常 |
| RocketMQ单个Broker主节点宕机演练 | 本场景模拟RocketMQ单个Broker主节点宕机和主从切换场景，验证确认故障期间及恢复后，接入系统是否具备重连重试能力，消息生产和消费逻辑是否正常 |
| RocketMQ（容灾模式）容灾切换演练 | 本场景模拟RocketMQ容灾模式主机房全量宕机场景，验证接入系统是否可成功完成手动容灾切换，消息生产和消费逻辑是否正常 |
| RocketMQ消息堆积演练 | 本场景模拟生产者大量生产消息，RocketMQ消息堆积场景，验证RocketMQ容量是否充足，接入系统是否可通过横向扩容消费者处理消息堆积问题 |
