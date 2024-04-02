# Script to enrich the conn.log with ASN number and ASN name

export {
    redef record Conn::Info += {
        orig_h_asn: geo_autonomous_system &log &optional;
        resp_h_asn: geo_autonomous_system &log &optional;
    };
}

event connection_state_remove(c: connection) &priority=0
{
    if (!c?$conn || !c$conn?$id) return;

    local orig_h = c$conn$id$orig_h;
    local resp_h = c$conn$id$resp_h;

    if (!Site::is_private_addr(orig_h)) {
        c$conn$orig_h_asn = lookup_autonomous_system(orig_h);
    }

    if (!Site::is_private_addr(resp_h)) {
        c$conn$resp_h_asn = lookup_autonomous_system(resp_h);
    }
}
