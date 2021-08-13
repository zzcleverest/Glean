const url = window.location.href;
ct = url.substr(url.lastIndexOf("/") + 1)
// 基于准备好的dom，初始化echarts实例
var graphChart = echarts.init(document.getElementById('event_graph'));
var eventChart = echarts.init(document.getElementById('event'));
var actorChart = echarts.init(document.getElementById('actor'));
var IR_options = ['Demand economic aid', 'DEMAND', 'DISAPPROVE', 'REJECT', 'THREATEN', 'PROTEST', 'EXHIBIT FORCE POSTURE', 'REDUCE RELATIONS', 'COERCE', 'ASSAULT', 'FIGHT', 'USE UNCONVENTIONAL MASS VIOLENCE', 'Appeal for material cooperation, not specified below', 'Appeal for diplomatic cooperation (such as policy support)', 'Appeal for aid, not specified below', 'Demand change in institutions, regime', 'Appeal to yield, not specified below', 'Appeal to others to meet or negotiate', 'Appeal to others to settle dispute', 'Appeal to engage in or accept mediation', 'Demand release of persons or property', 'Express intent to cooperate, not specified below', 'Express intent to engage in material cooperation, not specified below', 'Express intent to engage in diplomatic cooperation (such as policy support)', 'Express intent to provide material aid, not specified below', 'Demand de-escalation of military engagement', 'Express intent to yield, not specified below', 'Express intent to meet or negotiate', 'Express intent to settle dispute', 'Express intent to institute political reform, not specified below', 'Express intent to mediate', 'Consult, not specified below', 'Discuss by telephone', 'Make a visit', 'Host a visit', 'Meet at a third location', 'Mediate', 'Engage in negotiatio', 'Express intent to accept mediation', 'Engage in diplomatic cooperation, not specified below', 'Praise or endorse', 'Defend verbally', 'Rally support on behalf of', 'Grant diplomatic recognition', 'Apologize', 'Forgive', 'Sign formal agreement', 'Engage in material cooperation, not specified below', 'Cooperate economically', 'Cooperate militarily', 'Engage in judicial cooperation', 'Share intelligence or information', 'Provide aid, not specified below', 'Provide economic aid', 'Provide military aid', 'Provide humanitarian aid', 'Provide military protection or peacekeeping', 'Grant asylum', 'Yield, not specified below', 'Ease administrative sanctions, not specified below', 'Ease political dissent', 'Accede to requests or demands for political reform, not specified below', 'Return, release, not specified below', 'Ease economic sanctions, boycott, embargo', 'Allow international involvement, not specified below', 'De-escalate military engagement', 'Reduce or stop military assistance', 'Reduce or stop economic assistance', 'Investigate, not specified below', 'Investigate crime, corruption', 'Investigate human rights abuses', 'Investigate military action', 'Investigate war crimes', 'Accuse of crime, corruption', 'Accuse of human rights abuses', 'Accuse of aggression', 'Demand, not specified below', 'Demand material cooperation, not specified below', 'Accuse of war crimes', 'Accuse of espionage, treason', 'Demand diplomatic cooperation (such as policy support)', 'Demand that target yields, not specified below', 'Demand meeting, negotiation', 'Reject request or demand for political reform, not specified below', 'Disapprove, not specified below', 'Criticize or denounce', 'Accuse, not specified below', 'Rally opposition against', 'Complain o\x0ecially', 'Bring lawsuit against', 'Demand change in leadership', 'Reject, not specified below', 'Reject material cooperation', 'Reject request or demand for material aid, not specified below', 'Demand policy change', 'Refuse to yield, not specified below', 'Reject proposal to meet, discuss, or negotiate', 'Expel or withdraw peacekeepers', 'Reject plan, agreement to settle dispute', 'Defy norms, law', 'Veto', 'Threaten, not specified below', 'Threaten non-force, not specified below', 'Expel or withdraw inspectors, observers', 'Threaten with political dissent, protest', 'Threaten to halt negotiations', 'Threaten with administrative sanctions, not specified below', 'Threaten to halt international involvement (non-mediation)', 'Demand rights', 'Threaten with military force, not specified below', 'Give ultimatum', 'Engage in political dissent, not specified below', 'Demonstrate or rally, not specified below', 'Conduct hunger strike, not specified below', 'Conduct strike or boycott, not specified below', 'Obstruct passage, block, not specified below', 'Protest violently, riot, not specified below', 'Threaten with repression', 'Demonstrate military or police power, not specified below', 'Increase police alert status', 'Increase military alert status', 'Mobilize or increase police power', 'Mobilize or increase armed forces', 'Reduce relations, not specified below', 'Reduce or break diplomatic relations', 'Reduce or stop material aid, not specified below', 'Impose embargo, boycott, or sanctions', 'Halt negotiations', 'Expel or withdraw, not specified below', 'Coerce, not specified below', 'Seize or damage property, not specified below', 'Impose administrative sanctions, not specified below', 'Arrest, detain, or charge with legal action', 'Expel or deport individuals', 'Use tactics of violent repression', 'Destroy property', 'Confiscate property', 'Use unconventional violence, not specified below', 'Abduct, hijack, or take hostage', 'Physically assault, not specified below', 'Conduct suicide, car, or other non-military bombing, not specified below', 'Use as human shield', 'Attempt to assassinate', 'Ban political parties or politicians', 'Assassinate', 'Impose restrictions on political freedoms', 'Impose state of emergency or martial law', 'Use conventional military force, not specified below', 'Impose blockade, restrict movement', 'Occupy territory', 'Fight with small arms and light weapons', 'Fight with artillery and tanks', 'Employ aerial weapons, not specified below', 'Impose curfew', 'Violate ceasefire', 'Engage in mass expulsion', 'Engage in mass killings', 'Engage in ethnic cleansing', 'Reject request for change in leadership', 'Reject request for policy change', 'Reject request for rights', 'Appeal for economic cooperation', 'Appeal for military cooperation', 'Appeal for judicial cooperation', 'Appeal for intelligence', 'Refuse to ease administrative sanctions', 'Refuse to release persons or property', 'Refuse to ease economic sanctions, boycott, or embargo', 'Refuse to de-escalate military engagement', 'Appeal for economic aid', 'Appeal for military aid', 'Appeal for humanitarian aid', 'Appeal for military protection or peacekeeping', 'Appeal for change in leadership', 'Appeal for policy change', 'Appeal for rights', 'Appeal for change in institutions, regime', 'Appeal for easing of administrative sanctions', 'Appeal for release of persons or property', 'Appeal for de-escalation of military engagement', 'Sexually assault', 'Torture', 'Kill by physical assault', 'Threaten with sanctions, boycott, embargo', 'Threaten to reduce or break relations', 'Carry out suicide bombing', 'Carry out vehicular bombing', 'Ease restrictions on political freedoms', 'Express intent to cooperate economically', 'Express intent to cooperate militarily', 'Accede to demands for change in leadership', 'Accede to demands for rights', 'Return, release person(s)', 'Return, release property', 'Express intent to provide economic aid', 'Express intent to provide military aid', 'Express intent to provide humanitarian aid', 'Express intent to provide military protection or peacekeeping', 'Express intent to change leadership', 'Receive inspectors', 'Express intent to ease administrative sanctions', 'Express intent to release persons or property', 'Express intent to de-escalate military engagement', 'Threaten unconventional violence', 'Threaten conventional attack', 'Declare truce, ceasefire', 'Retreat or surrender militarily', 'Demobilize armed forces', 'Ease military blockade', 'Demonstrate for leadership change', 'Demonstrate for rights', 'Demand easing of economic sanctions, boycott, or embargo', 'Demand judicial cooperation', 'Demand intelligence cooperation']
var IZ_options = ['Demand economic aid', 'DEMAND', 'DISAPPROVE', 'REJECT', 'THREATEN', 'PROTEST', 'EXHIBIT FORCE POSTURE', 'REDUCE RELATIONS', 'COERCE', 'ASSAULT', 'FIGHT', 'USE UNCONVENTIONAL MASS VIOLENCE', 'Demand change in institutions, regime', 'Appeal for diplomatic cooperation (such as policy support)', 'Appeal for aid, not specified below', 'Demand rights', 'Appeal to yield, not specified below', 'Appeal to others to meet or negotiate', 'Appeal to others to settle dispute', 'Appeal to engage in or accept mediation', 'Demand release of persons or property', 'Express intent to cooperate, not specified below', 'Express intent to engage in material cooperation, not specified below', 'Express intent to engage in diplomatic cooperation (such as policy support)', 'Express intent to provide material aid, not specified below', 'Demand de-escalation of military engagement', 'Express intent to yield, not specified below', 'Express intent to meet or negotiate', 'Express intent to settle dispute', 'Express intent to accept mediation', 'Express intent to mediate', 'Consult, not specified below', 'Discuss by telephone', 'Make a visit', 'Host a visit', 'Meet at a third location', 'Mediate', 'Engage in negotiatio', 'Engage in diplomatic cooperation, not specified below', 'Praise or endorse', 'Defend verbally', 'Rally support on behalf of', 'Grant diplomatic recognition', 'Apologize', 'Forgive', 'Sign formal agreement', 'Engage in material cooperation, not specified below', 'Cooperate economically', 'Cooperate militarily', 'Engage in judicial cooperation', 'Share intelligence or information', 'Provide aid, not specified below', 'Provide economic aid', 'Provide military aid', 'Provide humanitarian aid', 'Provide military protection or peacekeeping', 'Grant asylum', 'Yield, not specified below', 'Ease administrative sanctions, not specified below', 'Ease political dissent', 'Accede to requests or demands for political reform, not specified below', 'Return, release, not specified below', 'Ease economic sanctions, boycott, embargo', 'Allow international involvement, not specified below', 'De-escalate military engagement', 'Reduce or stop humanitarian assistance', 'Investigate, not specified below', 'Investigate crime, corruption', 'Investigate human rights abuses', 'Investigate military action', 'Investigate war crimes', 'Accuse of crime, corruption', 'Accuse of human rights abuses', 'Accuse of aggression', 'Demand, not specified below', 'Accuse of war crimes', 'Demand material cooperation, not specified below', 'Demand diplomatic cooperation (such as policy support)', 'Accuse of espionage, treason', 'Demand that target yields, not specified below', 'Appeal for material cooperation, not specified below', 'Disapprove, not specified below', 'Criticize or denounce', 'Accuse, not specified below', 'Rally opposition against', 'Complain o\x0ecially', 'Bring lawsuit against', 'Demand change in leadership', 'Reject, not specified below', 'Reject material cooperation', 'Reject request or demand for material aid, not specified below', 'Appeal for political reform, not specified below', 'Refuse to yield, not specified below', 'Reject proposal to meet, discuss, or negotiate', 'Demand policy change', 'Reject plan, agreement to settle dispute', 'Defy norms, law', 'Veto', 'Threaten, not specified below', 'Threaten non-force, not specified below', 'Threaten with political dissent, protest', 'Threaten to halt negotiations', 'Threaten to halt international involvement (non-mediation)', 'Threaten with military force, not specified below', 'Give ultimatum', 'Engage in political dissent, not specified below', 'Demonstrate or rally, not specified below', 'Conduct hunger strike, not specified below', 'Conduct strike or boycott, not specified below', 'Obstruct passage, block, not specified below', 'Protest violently, riot, not specified below', 'Demonstrate military or police power, not specified below', 'Increase police alert status', 'Increase military alert status', 'Mobilize or increase police power', 'Mobilize or increase armed forces', 'Reduce relations, not specified below', 'Reduce or break diplomatic relations', 'Reduce or stop material aid, not specified below', 'Impose embargo, boycott, or sanctions', 'Halt negotiations', 'Expel or withdraw, not specified below', 'Coerce, not specified below', 'Seize or damage property, not specified below', 'Impose administrative sanctions, not specified below', 'Arrest, detain, or charge with legal action', 'Expel or deport individuals', 'Use tactics of violent repression', 'Destroy property', 'Confiscate property', 'Express intent to institute political reform, not specified below', 'Use unconventional violence, not specified below', 'Abduct, hijack, or take hostage', 'Physically assault, not specified below', 'Conduct suicide, car, or other non-military bombing, not specified below', 'Use as human shield', 'Impose restrictions on political freedoms', 'Assassinate', 'Attempt to assassinate', 'Impose state of emergency or martial law', 'Impose curfew', 'Use conventional military force, not specified below', 'Impose blockade, restrict movement', 'Occupy territory', 'Fight with small arms and light weapons', 'Fight with artillery and tanks', 'Employ aerial weapons, not specified below', 'Reject economic cooperation', 'Engage in mass expulsion', 'Engage in mass killings', 'Engage in ethnic cleansing', 'Reject request for rights', 'Appeal for economic cooperation', 'Appeal for judicial cooperation', 'Appeal for intelligence', 'Refuse to ease administrative sanctions', 'Refuse to release persons or property', 'Refuse to ease economic sanctions, boycott, or embargo', 'Refuse to de-escalate military engagement', 'Appeal for economic aid', 'Appeal for military aid', 'Appeal for humanitarian aid', 'Appeal for military protection or peacekeeping', 'Appeal for change in leadership', 'Appeal for rights', 'Appeal for change in institutions, regime', 'Appeal for release of persons or property', 'Appeal for de-escalation of military engagement', 'Sexually assault', 'Torture', 'Kill by physical assault', 'Threaten with sanctions, boycott, embargo', 'Threaten to reduce or break relations', 'Carry out suicide bombing', 'Carry out vehicular bombing', 'Ease restrictions on political freedoms', 'Ease curfew', 'Ease state of emergency or martial law', 'Express intent to cooperate economically', 'Express intent to cooperate militarily', 'Accede to demands for change in leadership', 'Accede to demands for rights', 'Return, release person(s)', 'Return, release property', 'Express intent to provide economic aid', 'Express intent to provide military aid', 'Express intent to provide humanitarian aid', 'Express intent to provide military protection or peacekeeping', 'Express intent to change leadership', 'Receive deployment of peacekeepers', 'Receive inspectors', 'Express intent to release persons or property', 'Express intent to de-escalate military engagement', 'Declare truce, ceasefire', 'Threaten conventional attack', 'Demobilize armed forces', 'Retreat or surrender militarily', 'Threaten unconventional violence', 'Demonstrate for leadership change', 'Ban political parties or politicians', 'Demand intelligence cooperation']
var TU_options = ['Demand economic aid', 'DEMAND', 'DISAPPROVE', 'REJECT', 'THREATEN', 'PROTEST', 'EXHIBIT FORCE POSTURE', 'REDUCE RELATIONS', 'COERCE', 'ASSAULT', 'Demand rights', 'USE UNCONVENTIONAL MASS VIOLENCE', 'Appeal for material cooperation, not specified below', 'Appeal for diplomatic cooperation (such as policy support)', 'Appeal for aid, not specified below', 'FIGHT', 'Appeal to yield, not specified below', 'Appeal to others to meet or negotiate', 'Appeal to others to settle dispute', 'Appeal to engage in or accept mediation', 'Demand change in institutions, regime', 'Express intent to cooperate, not specified below', 'Express intent to engage in material cooperation, not specified below', 'Express intent to engage in diplomatic cooperation (such as policy support)', 'Express intent to provide material aid, not specified below', 'Demand de-escalation of military engagement', 'Express intent to yield, not specified below', 'Express intent to meet or negotiate', 'Express intent to institute political reform, not specified below', 'Express intent to accept mediation', 'Express intent to mediate', 'Consult, not specified below', 'Discuss by telephone', 'Make a visit', 'Host a visit', 'Meet at a third location', 'Mediate', 'Engage in negotiatio', 'Engage in diplomatic cooperation, not specified below', 'Praise or endorse', 'Defend verbally', 'Rally support on behalf of', 'Grant diplomatic recognition', 'Apologize', 'Forgive', 'Sign formal agreement', 'Engage in material cooperation, not specified below', 'Cooperate economically', 'Cooperate militarily', 'Engage in judicial cooperation', 'Share intelligence or information', 'Provide aid, not specified below', 'Provide economic aid', 'Provide military aid', 'Provide humanitarian aid', 'Provide military protection or peacekeeping', 'Grant asylum', 'Yield, not specified below', 'Ease administrative sanctions, not specified below', 'Ease political dissent', 'Accede to requests or demands for political reform, not specified below', 'Return, release, not specified below', 'Ease economic sanctions, boycott, embargo', 'Allow international involvement, not specified below', 'De-escalate military engagement', 'Reduce or stop economic assistance', 'Reduce or stop military assistance', 'Investigate, not specified below', 'Investigate crime, corruption', 'Investigate human rights abuses', 'Investigate military action', 'Investigate war crimes', 'Reduce or stop humanitarian assistance', 'Accuse of crime, corruption', 'Accuse of human rights abuses', 'Accuse of aggression', 'Demand, not specified below', 'Accuse of war crimes', 'Accuse of espionage, treason', 'Demand material cooperation, not specified below', 'Demand diplomatic cooperation (such as policy support)', 'Demand that target yields, not specified below', 'Demand meeting, negotiation', 'Demand settling of dispute', 'Disapprove, not specified below', 'Criticize or denounce', 'Accuse, not specified below', 'Rally opposition against', 'Complain o\x0ecially', 'Bring lawsuit against', 'Find guilty or liable (legally)', 'Demand change in leadership', 'Reject, not specified below', 'Appeal for political reform, not specified below', 'Reject request or demand for material aid, not specified below', 'Reject request or demand for political reform, not specified below', 'Refuse to yield, not specified below', 'Reject proposal to meet, discuss, or negotiate', 'Reject mediation', 'Reject plan, agreement to settle dispute', 'Defy norms, law', 'Veto', 'Threaten, not specified below', 'Threaten non-force, not specified below', 'Expel or withdraw inspectors, observers', 'Threaten with political dissent, protest', 'Threaten to halt negotiations', 'Threaten to halt international involvement (non-mediation)', 'Threaten with repression', 'Threaten with military force, not specified below', 'Give ultimatum', 'Engage in political dissent, not specified below', 'Demonstrate or rally, not specified below', 'Conduct hunger strike, not specified below', 'Conduct strike or boycott, not specified below', 'Obstruct passage, block, not specified below', 'Protest violently, riot, not specified below', 'Demonstrate military or police power, not specified below', 'Increase police alert status', 'Increase military alert status', 'Mobilize or increase police power', 'Mobilize or increase armed forces', 'Reduce relations, not specified below', 'Reduce or break diplomatic relations', 'Reduce or stop material aid, not specified below', 'Impose embargo, boycott, or sanctions', 'Halt negotiations', 'Expel or withdraw, not specified below', 'Coerce, not specified below', 'Seize or damage property, not specified below', 'Impose administrative sanctions, not specified below', 'Arrest, detain, or charge with legal action', 'Expel or deport individuals', 'Use tactics of violent repression', 'Destroy property', 'Confiscate property', 'Demand release of persons or property', 'Use unconventional violence, not specified below', 'Abduct, hijack, or take hostage', 'Physically assault, not specified below', 'Conduct suicide, car, or other non-military bombing, not specified below', 'Demand easing of economic sanctions, boycott, or embargo', 'Attempt to assassinate', 'Assassinate', 'Impose curfew', 'Impose restrictions on political freedoms', 'Express intent to settle dispute', 'Use conventional military force, not specified below', 'Impose blockade, restrict movement', 'Occupy territory', 'Fight with small arms and light weapons', 'Fight with artillery and tanks', 'Employ aerial weapons, not specified below', 'Impose state of emergency or martial law', 'Violate ceasefire', 'Unknown', 'Engage in mass expulsion', 'Engage in mass killings', 'Engage in ethnic cleansing', 'Reject request for rights', 'Appeal for economic cooperation', 'Appeal for judicial cooperation', 'Appeal for intelligence', 'Refuse to ease administrative sanctions', 'Refuse to release persons or property', 'Refuse to ease economic sanctions, boycott, or embargo', 'Refuse to de-escalate military engagement', 'Appeal for economic aid', 'Appeal for military aid', 'Appeal for humanitarian aid', 'Appeal for military protection or peacekeeping', 'Appeal for change in leadership', 'Appeal for rights', 'Appeal for change in institutions, regime', 'Appeal for easing of administrative sanctions', 'Appeal for release of persons or property', 'Appeal for easing of economic sanctions, boycott, or embargo', 'Appeal for de-escalation of military engagement', 'Sexually assault', 'Torture', 'Kill by physical assault', 'Threaten with sanctions, boycott, embargo', 'Threaten to reduce or break relations', 'Threaten to reduce or stop aid', 'Carry out suicide bombing', 'Carry out vehicular bombing', 'Threaten to ban political parties or politicians', 'Ease restrictions on political freedoms', 'Ease curfew', 'Express intent to cooperate economically', 'Express intent to cooperate militarily', 'Express intent to cooperate on intelligence', 'Accede to demands for change in leadership', 'Accede to demands for rights', 'Accede to demands for change in institutions, regime', 'Return, release person(s)', 'Return, release property', 'Express intent to provide economic aid', 'Express intent to provide military aid', 'Express intent to provide humanitarian aid', 'Express intent to provide military protection or peacekeeping', 'Express intent to change leadership', 'Receive deployment of peacekeepers', 'Receive inspectors', 'Express intent to ease administrative sanctions', 'Allow humanitarian access', 'Express intent to release persons or property', 'Express intent to allow international involvement (non-mediation)', 'Express intent to de-escalate military engagement', 'Declare truce, ceasefire', 'Threaten conventional attack', 'Demobilize armed forces', 'Retreat or surrender militarily', 'Ease military blockade', 'Threaten unconventional violence', 'Demonstrate for leadership change', 'Ban political parties or politicians', 'Reject material cooperation', 'Demand judicial cooperation', 'Demand intelligence cooperation']

if (ct == 'IR') {
    for (i = 0; i < IR_options.length; ++i) {
        var option = $("<option />");
        option.html(i + ' ' + IR_options[i]);
        option.val(IR_options[i]);
        $("#select").append(option);
    }
} else if (ct == 'IZ') {
    for (i = 0; i < IZ_options.length; ++i) {
        var option = $("<option />");
        option.html(i + ' ' + IZ_options[i]);
        option.val(IZ_options[i]);
        $("#select").append(option);
    }
} else {
    for (i = 0; i < TU_options.length; ++i) {
        var option = $("<option />");
        option.html(i + ' ' + TU_options[i]);
        option.val(TU_options[i]);
        $("#select").append(option);
    }
}


function draw_event_graph(val) {
    var categories = [];
    for (var i = 0; i < val.node_data.length; i++) {
        categories[i] = {
            name: 'type' + i
        };
    }
    option = {
        // 图的标题
        title: {
            text: '事件图'
        },
        // 提示框的配置
        tooltip: {
            formatter: function (x) {
                return x.data.des;
            }
        },
        // 工具箱
        toolbox: {
            // 显示工具箱
            show: true,
            feature: {
                mark: {
                    show: true
                },
                // 还原
                restore: {
                    show: true
                },
                // 保存为图片
                saveAsImage: {
                    show: true
                }
            }
        },
        legend: [],
        series: [{
            type: 'graph', // 类型:关系图
            layout: 'force', //图的布局，类型为力导图
            symbolSize: 40, // 调整节点的大小
            roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [2, 10],
            edgeLabel: {
                normal: {
                    textStyle: {
                        fontSize: 20
                    }
                }
            },
            force: {
                repulsion: 2500,
                edgeLength: [10, 50]
            },
            draggable: true,
            lineStyle: {
                normal: {
                    width: 2,
                    color: '#4b565b',
                }
            },
            edgeLabel: {
                normal: {
                    show: true,
                    formatter: function (x) {
                        return x.data.name;
                    }
                }
            },
            label: {
                normal: {
                    show: true,
                    textStyle: {}
                }
            },

            // 数据
            data: val['node_data'],
            links: val['relation_data'],
            categories: categories,
        }]
    };
    graphChart.setOption(option);
};

function draw_event(val) {
    // console.log(`data is ${val}`);
    var option = {
        title: {
            text: '多事件预测'
        },
        tooltip: {},
        legend: [],
        xAxis: {
            data: val['event_x_data']
        },
        yAxis: {},
        series: [{
            name: 'prob',
            type: 'bar',
            data: val['event_y_data']
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    eventChart.setOption(option);
};

function draw_actor(val) {
    // console.log(`data is ${val}`);
    // console.log(`data is ${val}`);
    var categories = [];
    for (var i = 0; i < val.actor_node_data.length; i++) {
        categories[i] = {
            name: 'type' + i
        };
    }
    option = {
        // 图的标题
        title: {
            text: '多参与者预测'
        },
        // 提示框的配置
        tooltip: {
            formatter: function (x) {
                return x.data.des;
            }
        },
        // 工具箱
        toolbox: {
            // 显示工具箱
            show: true,
            feature: {
                mark: {
                    show: true
                },
                // 还原
                restore: {
                    show: true
                },
                // 保存为图片
                saveAsImage: {
                    show: true
                }
            }
        },
        legend: [],
        series: [{
            type: 'graph', // 类型:关系图
            layout: 'force', //图的布局，类型为力导图
            symbolSize: 40, // 调整节点的大小
            roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [2, 10],
            edgeLabel: {
                normal: {
                    textStyle: {
                        fontSize: 20
                    }
                }
            },
            force: {
                repulsion: 2500,
                edgeLength: [10, 50]
            },
            draggable: true,
            lineStyle: {
                normal: {
                    width: 2,
                    color: '#4b565b',
                }
            },
            edgeLabel: {
                normal: {
                    show: true,
                    formatter: function (x) {
                        return x.data.name;
                    }
                }
            },
            label: {
                normal: {
                    show: true,
                    textStyle: {}
                }
            },

            // 数据
            data: val['actor_node_data'],
            links: val['actor_relation_data'],
            categories: categories,
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    actorChart.setOption(option);
};


function get_data(val) {
    data = {
        date: val
    }
    $.post('http://106.52.65.202/t5/api/' + ct + '/graph', data, function (data, status) {
        //console.log(`${data} and status is ${status}`);
        data = JSON.parse(data);
        draw_event_graph(data);
    });
    $.post('http://106.52.65.202/t5/api/' + ct + '/event', data, function (data, status) {
        //console.log(`${data} and status is ${status}`);
        data = JSON.parse(data);
        draw_event(data);
    });
    //    $.post('http://106.52.65.202/t5/api/' + ct + '/actor', data, function (data, status) {
    //        //console.log(`${data} and status is ${status}`);
    //        data = JSON.parse(data);
    //        draw_actor(data);
    //    });
};


function draw_chart(val) {
    get_data(val);
};

function draw_actor_chart() {
    tm = $("#calendar").val();
    rel = $("#select").val();
    if (ct == 'IR') {
        options = IR_options;
    } else if (ct == 'IZ') {
        options = IZ_options;
    } else if (ct == 'TU') {
        options = TU_options;
    }
    rel_index = -1;
    for (i = 0; i < options.length; ++i) {
        if (options[i] == rel) {
            rel_index = i;
            break;
        }
    }
    data = {
        date: tm,
        relation: rel_index,
        name: rel
    }
    console.log(data);
    $.post('http://106.52.65.202/t5/api/' + ct + '/actor', data, function (data, status) {
        //console.log(`${data} and status is ${status}`);
        data = JSON.parse(data);
        draw_actor(data);
    });
}
