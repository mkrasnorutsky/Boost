#include <boost/version.hpp>
#include <boost/bimap.hpp>
#include <boost/multi_index_container.hpp>
#include <boost/multi_index/member.hpp>
#include <boost/multi_index/ordered_index.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/optional.hpp>
#include <boost/tokenizer.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <sstream>
#include <string>
#include <vector>
extern "C" unsigned int OneClickPilotBoostVersion(void);
struct Aircraft { int id; std::string name; };
using Fleet = boost::multi_index_container<Aircraft, boost::multi_index::indexed_by<
    boost::multi_index::ordered_unique<boost::multi_index::member<Aircraft,int,&Aircraft::id>>>>;
int main() {
    static_assert(BOOST_VERSION == 108600, "Expected Boost 1.86.0");
    if (OneClickPilotBoostVersion() != BOOST_VERSION) return 1;
    boost::bimap<int,std::string> controls;
    controls.insert({1,"pitch"});
    if (controls.right.at("pitch") != 1) return 2;
    Fleet fleet; fleet.insert({172,"C172P"});
    if (fleet.find(172)->name != "C172P") return 3;
    boost::optional<int> heading = boost::lexical_cast<int>("270");
    if (!heading || *heading != 270) return 4;
    std::string input=" C172P,EGKA "; boost::trim(input);
    boost::char_separator<char> sep(","); boost::tokenizer<boost::char_separator<char>> tokens(input,sep);
    std::vector<std::string> parts(tokens.begin(),tokens.end());
    if (parts.size()!=2 || parts[1]!="EGKA") return 5;
    std::istringstream xml("<aircraft><name>C172P</name></aircraft>");
    boost::property_tree::ptree tree; boost::property_tree::read_xml(xml,tree);
    if (tree.get<std::string>("aircraft.name")!="C172P") return 6;
    return 0;
}
